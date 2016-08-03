# coding: utf-8
from pagseguro.api import PagSeguroItem, PagSeguroApi
from rest_framework.exceptions import APIException
from django.conf import settings
from datetime import datetime

def pay_pagseguro(data, payment, test=False):
    item1 = PagSeguroItem(id='0001', description='Pagamento', amount=data.get('value'), quantity=1)
    pagseguro_api = PagSeguroApi(reference='paymentserver', email=data.get('code'), token=data.get('key'))
    pagseguro_api.add_item(item1)
    response = pagseguro_api.checkout()
    # import pdb;pdb.set_trace()
    if response and response.get('status_code') == 200:
        payment.pagseguro_url = response.get('redirect_url')
        payment.pagseguro_code = response.get('code')
        payment.is_authorized = False
        payment.is_paid = False
        payment.save()
        return payment
    else:
        payment.status_code = response.get('status_code')
        payment.response_text = response.get('message')
        payment.paid_at = datetime.now()
        payment.is_authorized = False
        payment.is_paid = False
        payment.save()
        raise APIException(u'Erro %s' % response.get('message'))
