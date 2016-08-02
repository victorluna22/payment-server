# coding: utf-8
from decimal import Decimal
from datetime import datetime
from pyrcws import GetAuthorizedException, PaymentAttempt
from django.conf import settings
from rest_framework.exceptions import APIException


def authorize_redecard(data, payment):
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
        payment.save()
        raise APIException(u'Erro %s: %s' % (e.codret, e.msg))

    if attempt.msgret:
        payment.status_code = attempt.codret
        payment.response_text = attempt.msgret
        payment.numcv = attempt.numcv
        payment.numautor = attempt.numautor
        payment.is_authorized = True
        payment.save()

    return payment


def confirm_redecard(payment):
    params = {
        'affiliation_id': settings.REDECARD_SANDBOX_AFFILIATION_ID,
        'total': payment.value,
        'order_id': payment.id,
        'card_number': '',
        'cvc2': '',
        'exp_month': '',
        'exp_year': '',
        'card_holders_name': payment.name,
        'installments': 1,
        'debug': True,
    }

    attempt = PaymentAttempt(**params)
    attempt._authorized = True
    attempt.numautor = payment.numautor
    attempt.numcv = payment.numcv
    attempt.data = payment.created_at
    attempt.numsqn = 0
    attempt.msgret = payment.response_text
    attempt.codret = payment.status_code
    # import pdb;pdb.set_trace()
    # try:
    attempt.capture()
    # except:
    #     raise APIException(u'Transação não concluída')

    if attempt.msgret:
        payment.status_code = attempt.codret
        payment.response_text = attempt.msgret
        payment.paid_at = datetime.now()
        payment.is_paid = True
        payment.save()
    return payment


def pay_redecard(data, payment, test=False):
    params = {
        'affiliation_id': data.get('code'),
        'total': Decimal(data.get('value')),
        'order_id': payment.id,
        'card_number': data.get('number'),
        'cvc2': data.get('cvc'),
        'exp_month': data.get('expiration_month'),
        'exp_year': data.get('expiration_year'),
        'card_holders_name': data.get('name'),
        'installments': 1,
        'debug': test,
    }

    attempt = PaymentAttempt(**params)
    try:
        attempt.get_authorized(conftxn='S')
    except GetAuthorizedException, e:
        payment.status_code = attempt.codret
        payment.response_text = attempt.msgret
        payment.numcv = attempt.numcv
        payment.numautor = attempt.numautor
        payment.save()
        raise APIException(u'Erro %s: %s' % (e.codret, e.msg))
    else:
        attempt.capture()

    if attempt.msgret:
        payment.status_code = attempt.codret
        payment.response_text = attempt.msgret
        payment.paid_at = datetime.now()
        payment.is_authorized = True
        payment.is_paid = True
        payment.save()
    return payment