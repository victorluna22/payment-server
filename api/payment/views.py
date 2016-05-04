# coding: utf-8
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, PaymentProvider, TargetProvider
from .serializers import PaymentSerializer, BillingDataSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = BillingDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = PaymentProvider.objects.get_provider(request.data.get('provider_slug'))

        data = provider.pay(request.data)

        pay_serializer = PaymentSerializer(data)
        self.perform_create(serializer)

        headers = self.get_success_headers(pay_serializer.data)
        return Response(pay_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user.get_user()
        serializer.save(customer=user)

