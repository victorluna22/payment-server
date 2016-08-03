# coding: utf-8
import paypalrestsdk
from decimal import Decimal
from rest_framework.exceptions import APIException
from django.conf import settings
from datetime import datetime

def pay_paypal(data, payment, test=False):
    mode = 'sandbox' if test else 'live'
    paypalrestsdk.configure({
      "mode": mode, # sandbox or live
      "client_id": data.get('code'),
      "client_secret": data.get('key')})

    payment = make_payment(paypalrestsdk, data, payment)
    return payment


def make_payment(paypalrestsdk, data, payment):
    p = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
        "payment_method": "credit_card",
        "funding_instruments": [{
          "credit_card": {
            "type": data.get('card_type'),
            "number": data.get('number'),
            "expire_month": data.get('expiration_month'),
            "expire_year": data.get('expiration_year'),
            "cvv2": data.get('cvc'),
            "first_name": data.get('name').split(' ')[0],
            "last_name": ' '.join(data.get('name').split(' ')[1:])}}]},
      "transactions": [{
        "item_list": {
          "items": [{
            "name": "item",
            "sku": "item",
            "price": data.get('value'),
            "currency": "USD",
            "quantity": 1 }]},
        "amount": {
          "total": data.get('value'),
          "currency": "USD" },
        "description": "Pagamento" }]})
    # import pdb;pdb.set_trace()
    if p.create():
        payment.status_code = 0
        payment.response_text = u'Transação realizada com sucesso'
        payment.paid_at = datetime.now()
        payment.paypal_code = p.request_id
        payment.is_authorized = True
        payment.is_paid = True
        payment.save()
    else:
        payment.status_code = 1
        payment.response_text = p.error
        payment.save()
        print p.error
        raise APIException(u'Erro %s' % p.error)
    return payment