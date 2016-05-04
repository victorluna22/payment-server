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

        pay_serializer = PaymentSerializer(data=request.data)
        pay_serializer.is_valid(raise_exception=True)
        payment = pay_serializer.save(provider=provider)

        provider.pay(request.data, payment)

        headers = self.get_success_headers(pay_serializer.data)
        return Response(pay_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

