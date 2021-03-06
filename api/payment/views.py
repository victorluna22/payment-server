# coding: utf-8
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404
from .models import Payment, PaymentProvider
from .serializers import PaymentSerializer, BillingDataSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = BillingDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = PaymentProvider.objects.get_provider(request.data.get('provider_slug'))

        code, key = provider.get_auth(request.data, self.request.query_params.get('test'))
        if not code:
            raise APIException('Esta transação não possui credenciais de autenticação')

        pay_serializer = PaymentSerializer(data=request.data)
        pay_serializer.is_valid(raise_exception=True)
        payment = pay_serializer.save(provider=provider)

        data = pay_serializer.data

        data_post = request.data
        data_post['code'] = code
        data_post['key'] = key
        p = provider.pay(data_post, payment, self.request.query_params.get('test'))

        response = PaymentSerializer(p)

        headers = self.get_success_headers(response.data)
        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        queryset = Payment.objects.all()
        payment = get_object_or_404(queryset, payment_key=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


class PaymentAuthorizationCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = BillingDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = PaymentProvider.objects.get_provider(request.data.get('provider_slug'))

        pay_serializer = PaymentSerializer(data=request.data)
        pay_serializer.is_valid(raise_exception=True)
        payment = pay_serializer.save(provider=provider)

        payment = provider.authorize(request.data, payment)
        response = PaymentSerializer(payment)

        headers = self.get_success_headers(response.data)
        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)


class PaymentConfirmationView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, payment_key=self.request.POST.get('payment_key'))
        provider = PaymentProvider.objects.get_provider(payment.provider.slug)

        payment = provider.confirm(payment)
        response = PaymentSerializer(payment)

        headers = self.get_success_headers(response.data)
        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)