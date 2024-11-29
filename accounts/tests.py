import threading

from django.db import close_old_connections
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase, TransactionTestCase
from .models import Seller, PhoneNumber
from rest_framework import status


class RechargeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller = Seller.objects.create(name='Seller1', credit=100000)

    def test_recharge_successful(self):
        url = reverse('recharge-phone-number')
        data = {
            'seller_id': self.seller.id,
            'phone_number': "09372212589",
            'amount': 10000
        }
        response = self.client.post(url, data, format='json')
        self.seller.refresh_from_db()
        self.phone_number = PhoneNumber.objects.get(number="09372212589")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.seller.credit, 90000)
        self.assertEqual(self.phone_number.balance, 10000)

    def test_recharge_insufficient_credit(self):
        url = reverse('recharge-phone-number')
        data = {
            'seller_id': self.seller.id,
            'phone_number': "09372212589",
            'amount': 200000
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PerformanceTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller1 = Seller.objects.create(name='Seller1', credit=100000)
        self.seller2 = Seller.objects.create(name='Seller2', credit=100000)

    def perform_recharge_seller1(self):
        url = reverse('recharge-phone-number')
        data = {
            'seller_id': self.seller1.id,
            'phone_number': "09372212589",
            'amount': 10000
        }
        self.client.post(url, data, format='json')
        close_old_connections()

    def perform_recharge_seller2(self):
        url = reverse('recharge-phone-number')
        data = {
            'seller_id': self.seller2.id,
            'phone_number': "093888888",
            'amount': 10000
        }
        self.client.post(url, data, format='json')
        close_old_connections()

    def test_performance_under_high_load(self):
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=self.perform_recharge_seller1)
            threads.append(thread)
            thread.start()

            thread = threading.Thread(target=self.perform_recharge_seller2)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.credit, 100000 - 10000 * 5)

        self.seller2.refresh_from_db()
        self.assertEqual(self.seller2.credit, 100000 - 10000 * 5)