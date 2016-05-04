# coding: utf-8
from decimal import Decimal
from datetime import datetime
from cielo import PaymentAttempt, GetAuthorizedException
from django.conf import settings


def pay_cielo_test(data, payment):
    params = {
        'affiliation_id': settings.CIELO_SANDBOX_AFFILIATION_ID,
        'api_key': settings.CIELO_SANDBOX_API_KEY,
        'card_type': data.get('card_type'),
        'total': Decimal(data.get('value')),
        'order_id': payment.id,
        'card_number': data.get('number'),
        'cvc2': data.get('cvc'),
        'exp_month': data.get('expiration_month'),
        'exp_year': data.get('expiration_year'),
        'transaction': PaymentAttempt.CASH,
        'card_holders_name': data.get('name'),
        'installments': 1,
        'sandbox': True
    }

    attempt = PaymentAttempt(**params)
    try:
        attempt.get_authorized()
    except GetAuthorizedException, e:
        payment.status_code = 1000
        payment.response_text = e
        payment.paid_at = datetime.now()
        payment.save()
        print u'Não foi possível processar: %s' % e
    else:
        attempt.capture()
        payment.status_code = 0
        payment.paid_at = datetime.now()
        payment.response_text = u'Transação realizada com sucesso'
        payment.save()


def pay_cielo(data, payment):
    params = {
        'affiliation_id': settings.CIELO_AFFILIATION_ID,
        'api_key': settings.CIELO_API_KEY,
        'card_type': data.get('card_type'),
        'total': Decimal(data.get('value')),
        'order_id': payment.id,
        'card_number': data.get('number'),
        'cvc2': data.get('cvc'),
        'exp_month': data.get('expiration_month'),
        'exp_year': data.get('expiration_year'),
        'transaction': PaymentAttempt.CASH,
        'card_holders_name': data.get('name'),
        'installments': 1,
        'sandbox': False
    }

    attempt = PaymentAttempt(**params)
    try:
        attempt.get_authorized()
    except GetAuthorizedException, e:
        payment.status_code = 1000
        payment.response_text = e
        payment.paid_at = datetime.now()
        payment.save()
        print u'Não foi possível processar: %s' % e
    else:
        attempt.capture()
        payment.status_code = 0
        payment.paid_at = datetime.now()
        payment.response_text = u'Transação realizada com sucesso'
        payment.save()