from django.db import models

from accounts.models import Seller
from lib.base_model import BaseModel


class Orders(BaseModel):
    ORDER_TYPES = [
        ('credit', 'Credit Addition'),
        ('charge', 'Recharge Sale'),
    ]

    ORDER_STATUS = [
        ('PENDING', 'PENDING'),
        ('INQUIRY_PENDING', 'INQUIRY_PENDING'),
        ('DONE', 'DONE'),
        ('CANCEL', 'CANCEL'),
        ('TRANSACTION_FAILED', 'TRANSACTION_FAILED'),
        ('ORDER_FAILED', 'ORDER_FAILED'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    transaction_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=ORDER_STATUS)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.status} - {self.amount} for {self.seller.name}"
