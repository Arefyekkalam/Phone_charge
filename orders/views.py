from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from transactions.models import Transactions
from .models import Seller, Orders
from .serializers import IncreaseCreditSerializer

# TODO add api for get and search in orders and transactions for each seller and seller profile
# TODO handle auth and permissions

class CreditIncreaseRequestView(APIView):
    serializer_class = IncreaseCreditSerializer

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            seller_id = serializer.data.get('seller_id')
            amount = serializer.data.get('amount')
            description = serializer.data.get('description', '')

            order = Orders.objects.create(
                seller_id=seller_id,
                transaction_type='credit',
                amount=amount,
                status='PENDING',
                description=description
            )
            return Response({'order_id': order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO handle auth and permissions  ** only operators can approve orders
class ApproveCreditIncreaseView(APIView):
    def post(self, request, order_id):
        try:
            with transaction.atomic():
                order = Orders.objects.select_for_update().get(id=order_id, status='PENDING')
                seller = Seller.objects.select_for_update().get(id=order.seller_id)
                seller.credit += order.amount
                seller.save()
                order.status = 'DONE'
                order.save()
                Transactions.objects.create(
                    seller=seller,
                    order_id=order.id,
                    transaction_type='credit',
                    amount=order.amount,
                    status='DONE'
                )
            return Response({'message': 'Credit increased successfully.'}, status=status.HTTP_200_OK)
        except Orders.DoesNotExist:
            return Response({'error': 'Order not found or already processed.'}, status=status.HTTP_400_BAD_REQUEST)
