# coding: utf-8
from decimal import Decimal
from datetime import datetime
from cielo import PaymentAttempt, GetAuthorizedException
from rest_framework.exceptions import APIException
from django.conf import settings


def authorize_cielo(data, payment):
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
        payment.status_code = attempt.error_id
        payment.response_text = e
        payment.save()
        raise APIException(u'Erro %s' % e)
    else:
        payment.tid = attempt.transaction_id
        payment.status_code = 0
        payment.response_text = u'Autorizado com sucesso'
        payment.is_authorized = True
        payment.save()
    return payment


def confirm_cielo(payment):
    params = {
        'affiliation_id': settings.CIELO_SANDBOX_AFFILIATION_ID,
        'api_key': settings.CIELO_SANDBOX_API_KEY,
        'card_type': payment.card_type,
        'total': payment.value,
        'order_id': payment.id,
        'card_number': '',
        'cvc2': '',
        'exp_month': '',
        'exp_year': '',
        'transaction': PaymentAttempt.CASH,
        'card_holders_name': payment.name,
        'installments': 1,
        'sandbox': True
    }
    attempt = PaymentAttempt(**params)
    attempt.transaction_id = payment.tid
    attempt._authorized = True
    try:
        import pdb;pdb.set_trace()
        attempt.capture()
        payment.is_paid = True
        payment.status_code = 0
        payment.paid_at = datetime.now()
        payment.save()
    except:
        raise APIException(u'Transação não concluída')
    return payment


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
        payment.status_code = attempt.error_id
        payment.response_text = e
        payment.save()
        raise APIException(u'Erro %s' % e)
    else:
        attempt.capture()
        payment.status_code = 0
        payment.paid_at = datetime.now()
        payment.tid = attempt.transaction_id
        payment.is_authorized = True
        payment.is_paid = True
        payment.response_text = u'Transação realizada com sucesso'
        payment.save()
    return payment


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
        payment.status_code = attempt.error_id
        payment.response_text = e
        payment.save()
        raise APIException(u'Erro %s' % e)
    else:
        attempt.capture()
        payment.status_code = 0
        payment.paid_at = datetime.now()
        payment.tid = attempt.transaction_id
        payment.is_authorized = True
        payment.is_paid = True
        payment.response_text = u'Transação realizada com sucesso'
        payment.save()
    return payment