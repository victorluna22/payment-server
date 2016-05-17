# coding: utf-8
from pagseguro.api import PagSeguroItem, PagSeguroApi
from rest_framework.exceptions import APIException
from django.conf import settings
from datetime import datetime

def pay_pagseguro_test(data, payment):
    item1 = PagSeguroItem(id='0001', description='Pagamento', amount=data.get('value'), quantity=1)
    pagseguro_api = PagSeguroApi(reference='asdasdqwqwdsa', email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN)
    pagseguro_api.add_item(item1)
    response = pagseguro_api.checkout()
    # import pdb;pdb.set_trace()
    if response and response.get('status_code') == 200:
        payment.pagseguro_url = response.get('redirect_url')
        payment.pagseguro_code = response.get('code')
        payment.save()
        return response
    else:
        payment.status_code = response.get('status_code')
        payment.response_text = response.get('message')
        payment.paid_at = datetime.now()
        payment.save()
        raise APIException(u'Erro %s' % response.get('message'))


def pay_pagseguro(data, payment):
    pass