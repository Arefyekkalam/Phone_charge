import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Seller

logger = logging.getLogger(__name__)


class CreditAdditionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller = Seller.objects.create(name='Seller1', credit=10000)

    def test_credit_addition_success(self):
        url = reverse('credit-increase-request')
        data = {
            'seller_id': self.seller.id,
            'amount': 5000,
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
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 15000)

