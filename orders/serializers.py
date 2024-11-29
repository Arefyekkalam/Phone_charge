from django.db.models import DecimalField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from accounts.models import Seller
from orders.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class IncreaseCreditSerializer(serializers.Serializer):
    seller_id = PrimaryKeyRelatedField(queryset=Seller.objects.filter(is_active=True), required=True)
    amount = serializers.IntegerField(
        required=True,
    )
    description =  serializers.CharField(
        allow_null=True
    )