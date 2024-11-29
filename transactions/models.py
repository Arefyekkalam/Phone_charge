from django.db import models

from accounts.models import Seller
from lib.base_model import BaseModel
from orders.models import Orders


class Transactions(BaseModel):
    TRANSACTION_TYPES = [
        ('credit', 'Credit Addition'),
        ('charge', 'Recharge Sale'),
    ]

    TRANSACTION_STATUS = [
        ('DONE', 'DONE'),
        ('FAILED', 'FAILED'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=15, choices=TRANSACTION_STATUS)

    def __str__(self):
        return f"{self.status} - {self.amount} for {self.seller.name}"
