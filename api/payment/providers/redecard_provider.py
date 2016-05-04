# coding: utf-8
from decimal import Decimal
from datetime import datetime
from pyrcws import GetAuthorizedException, PaymentAttempt
from django.conf import settings
from rest_framework.exceptions import APIException


def pay_redecard_test(data, payment):
    params = {
        'affiliation_id': settings.REDECARD_SANDBOX_AFFILIATION_ID,
        'total': Decimal(data.get('value')),
        'order_id': payment.id,
        'card_number': data.get('number'),
        'cvc2': data.get('cvc'),
        'exp_month': data.get('expiration_month'),
        'exp_year': data.get('expiration_year'),
        'card_holders_name': data.get('name'),
        'installments': 1,
        'debug': True,
    }

    attempt = PaymentAttempt(**params)
    try:
        attempt.get_authorized(conftxn='S')
    except GetAuthorizedException, e:
        payment.status_code = attempt.codret
        payment.response_text = attempt.msgret
        payment.paid_at = datetime.now()
        payment.save()
        raise APIException(u'Erro %s: %s' % (e.codret, e.msg))
    else:
        attempt.capture()

    if attempt.msgret:
        payment.status_code = attempt.codret
        payment.response_text = attempt.msgret
        payment.paid_at = datetime.now()
        payment.save()
