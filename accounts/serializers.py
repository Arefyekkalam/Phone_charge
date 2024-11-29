from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from accounts.models import Seller, PhoneNumber


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'


class RechargePhoneNumberCreateSerializer(serializers.Serializer):
    seller_id = PrimaryKeyRelatedField(
        queryset=Seller.objects.filter(is_active=True),
        required=True
    )

    phone_number = serializers.CharField(
        required=True,
    )
    # TODO add phone_number validator

    amount = serializers.IntegerField(
        required=True,
    )
