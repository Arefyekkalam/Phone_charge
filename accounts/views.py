import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Seller, PhoneNumber
from accounts.serializers import RechargePhoneNumberCreateSerializer
from orders.models import Orders
from transactions.models import Transactions

logger = logging.getLogger(__name__)

# TODO handle add Api CRUD seller
# TODO handle auth and permissions
class RechargePhoneNumberView(APIView):
    serializer_class = RechargePhoneNumberCreateSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            seller_id = serializer.data.get('seller_id')
            phone_number = serializer.data.get('phone_number')
            amount = serializer.data.get('amount')
            logger.info(f"start, charge seller_id:{seller_id}, phone_number:{phone_number}")
            try:
                with transaction.atomic():
                    seller = Seller.objects.select_for_update().get(id=seller_id)
                    if seller.credit < amount:
                        Orders.objects.create(
                            seller=seller,
                            transaction_type='charge',
                            amount=amount,
                            status='ORDER_FAILED',
                            description="Low credit"
                        )
                        return Response({'error': _('Low credit.')}, status=status.HTTP_400_BAD_REQUEST)

                    phone, created = PhoneNumber.objects.select_for_update().get_or_create(number=phone_number, seller=seller)
                    phone.balance += amount
                    phone.save()

                    seller.credit -= amount
                    seller.save()

                    order_instance = Orders.objects.create(
                        seller=seller,
                        transaction_type='charge',
                        amount=amount,
                        status='DONE',
                        description="Phone charge"
                    )
                    Transactions.objects.create(
                        seller=seller,
                        order=order_instance,
                        transaction_type='charge',
                        amount=amount,
                        status='DONE',
                    )

                return Response({'message': _('Phone number recharged successfully.')}, status=status.HTTP_200_OK)
            except Seller.DoesNotExist:
                return Response({'error': _('Seller not found.')}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
