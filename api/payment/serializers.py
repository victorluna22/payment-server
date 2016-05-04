# coding: utf-8

from rest_framework import serializers
from .models import Payment, PaymentProvider


class PaymentProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentProvider


class PaymentSerializer(serializers.ModelSerializer):
    payment_key = serializers.UUIDField(format='hex_verbose')
    provider = PaymentProviderSerializer(required=False)

    class Meta:
        model = Payment
        fields = ('payment_key', 'provider', 'value', 'name', 'cpf', 'installments', 'status_code', 'created_at', 'paid_at')
        read_only_fields = ('created_at',)


class BillingDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    number = serializers.CharField(max_length=16)
    cpf = serializers.CharField(max_length=14)
    expiration = serializers.CharField(max_length=7)
    cvc = serializers.CharField(max_length=4)
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    installments = serializers.IntegerField(default=1)
