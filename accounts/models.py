from lib.base_model import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Seller(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    credit = models.DecimalField(verbose_name=_('credit'), max_digits=12, decimal_places=2, default=0.0)
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    number = models.CharField(max_length=15, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='phone_numbers')

    def __str__(self):
        return self.number