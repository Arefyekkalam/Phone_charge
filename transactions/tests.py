import threading

from django.db import close_old_connections
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Seller

# TODO handle data base connection single-tone
class ParallelTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller1 = Seller.objects.create(name='Seller1', credit=0)
        self.seller2 = Seller.objects.create(name='Seller2', credit=0)

    def perform_recharge(self, seller_id, amount, phone_number):
        url = reverse('recharge-phone-number')
        data = {
            'seller_id': seller_id,
            'phone_number': phone_number,
            'amount': amount
        }
        self.client.post(url, data, format='json')
        close_old_connections()

    def perform_credit_increase(self, seller_id, amount):
        url = reverse('credit-increase-request')
        data = {
            'seller_id': seller_id,
            'amount': amount,
            'description': "test_case"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_id = response.json().get("order_id")
        self.assertIsNotNone(order_id)

        url = reverse('approve-credit-increase', args=[order_id])
        data = {
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        close_old_connections()

    def test_parallel_case(self):

        threads = []
        for _ in range(5):
            thread1 = threading.Thread(target=self.perform_credit_increase, args=(self.seller1.id, 100000))
            thread2 = threading.Thread(target=self.perform_credit_increase, args=(self.seller2.id, 100000))

            threads.append(thread1)
            threads.append(thread2)

            thread1.start()
            thread2.start()

        for thread in threads:
            thread.join()

        for _ in range(10):
            thread1 = threading.Thread(target=self.perform_recharge, args=(self.seller1.id, 1000, "09372212589"))
            thread2 = threading.Thread(target=self.perform_recharge, args=(self.seller2.id, 1000, "09125097797"))

            threads.append(thread1)
            threads.append(thread2)

            thread1.start()
            thread2.start()

        for thread in threads:
            thread.join()

        self.seller1.refresh_from_db()
        self.seller2.refresh_from_db()

        self.assertEqual(self.seller1.credit, 5 * 100000 - 1000 * 10)
        self.assertEqual(self.seller2.credit, 5 * 100000 - 1000 * 10)
