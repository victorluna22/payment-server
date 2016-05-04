# -*- coding: utf-8 -*-
import uuid
from django.db import models


class PaymentProvider(models.Model):
    name = models.CharField('Nome do Provedor', max_length=255)
    slug = models.SlugField('Slug')
    status = models.BooleanField('Status', default=1)

    class Meta:
        verbose_name = u'Provedor de pagamento'
        verbose_name_plural = u'Provedores de pagamento'

    def __unicode__(self):
        return self.name


class TargetProvider(models.Model):
    provider = models.ForeignKey(PaymentProvider)

    class Meta:
        verbose_name = u'Provedor Default'
        verbose_name_plural = u'Provedores Default'


class Payment(models.Model):
    payment_key = models.CharField(max_length=64, verbose_name=u"Chave", unique=True)
    provider = models.ForeignKey(PaymentProvider)
    value = models.DecimalField(u'Valor', max_digits=9, decimal_places=2, default=0)
    status_code = models.IntegerField('Código de retorno', null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(verbose_name=u'Pago em', null=True, blank=True)

    class Meta:
        verbose_name = u'Pagamento'
        verbose_name_plural = u'Pagamentos'