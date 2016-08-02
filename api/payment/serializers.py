# coding: utf-8

from rest_framework import serializers
from .models import Payment, PaymentProvider, VISA, MASTERCARD, DINERS, DISCOVER, ELO, AMEX


class PaymentProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentProvider
        fields = ('name', 'slug', 'status')


class PaymentSerializer(serializers.ModelSerializer):
    payment_key = serializers.UUIDField(format='hex_verbose', required=False)
    provider = PaymentProviderSerializer(required=False)

    class Meta:
        model = Payment
        fields = ('payment_key', 'provider', 'value', 'name', 'cpf', 'project', 'installments', 'card_type', 'status_code', 'response_text', 'is_authorized', 'is_paid', 'created_at', 'paid_at')
        read_only_fields = ('created_at', 'response_text')


class BillingDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    number = serializers.CharField(max_length=16)
    cpf = serializers.CharField(max_length=14)
    expiration_month = serializers.IntegerField(max_value=12, min_value=1)
    expiration_year = serializers.IntegerField()
    cvc = serializers.CharField(max_length=4)
    card_type = serializers.CharField(max_length=30)
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    installments = serializers.IntegerField(default=1)

    def validate_card_type(self, type):
        if not type in [VISA, MASTERCARD, DINERS, DISCOVER, ELO, AMEX]:
            raise serializers.ValidationError("Bandeira do cartão inválida.")
        return type
