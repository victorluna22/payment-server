# -*- coding: utf-8 -*-
import uuid
from django.db import models
from .providers.cielo_provider import pay_cielo_test, pay_cielo
from .providers.redecard_provider import pay_redecard_test, pay_redecard
from .providers.pagseguro_provider import pay_pagseguro_test, pay_pagseguro

CIELO, REDECARD, PAGSEGURO = 'cielo', 'redecard', 'pagseguro'


class PaymentProviderManager(models.Manager):

    def get_provider(self, slug = None):
        if slug:
            provider = PaymentProvider.objects.get(slug=slug)
            if not provider.status:
                provider = self.get_any_provider()
        else:
            if TargetProvider.objects.all().exists():
                provider = TargetProvider.objects.all().order_by('-id')[0].provider
            else:
                provider = self.get_any_provider()
        return provider

    def get_any_provider(self):
        if PaymentProvider.objects.filter(status=1):
            return PaymentProvider.objects.filter(status=1)[0]


class PaymentProvider(models.Model):
    name = models.CharField('Nome do Provedor', max_length=255)
    slug = models.SlugField('Slug')
    status = models.BooleanField('Ativo?', default=1)

    objects = PaymentProviderManager()

    class Meta:
        verbose_name = u'Provedor de pagamento'
        verbose_name_plural = u'Provedores de pagamento'

    def __unicode__(self):
        return self.name

    def pay(self, data, payment):
        if self.slug == CIELO:
            return pay_cielo_test(data, payment)
        elif self.slug == REDECARD:
            return pay_redecard_test(data, payment)
        elif self.slug == PAGSEGURO:
            return pay_pagseguro_test(data, payment)


class TargetProvider(models.Model):
    provider = models.ForeignKey(PaymentProvider, verbose_name='Provedor')
    updated_at = models.DateTimeField(verbose_name='Última atualização', auto_now=True)

    class Meta:
        verbose_name = u'Chavear Provedor'
        verbose_name_plural = u'Chavear Provedor'

    def __unicode__(self):
        return self.provider.name


VISA, MASTERCARD, DINERS, DISCOVER, ELO, AMEX = 'visa', 'mastercard', 'diners', 'discover', 'elo', 'amex'
CARD_TYPES = (
    (VISA, 'Visa'),
    (MASTERCARD, 'Mastercard'),
    (DINERS, 'Diners'),
    (DISCOVER, 'Discover'),
    (ELO, 'Elo'),
    (AMEX, 'Amex'),
)


class Payment(models.Model):
    payment_key = models.UUIDField(verbose_name='Chave de pagamento', max_length=64, default=uuid.uuid4, editable=False, unique=True)
    provider = models.ForeignKey(PaymentProvider, verbose_name='Provedor')
    value = models.DecimalField(u'Valor', max_digits=9, decimal_places=2, default=0)
    status_code = models.IntegerField('Código de retorno', null=True, blank=True, db_index=True)
    name = models.CharField('Nome', max_length=100)
    card_type = models.CharField('Bandeira', max_length=30, choices=CARD_TYPES)
    cpf = models.CharField('CPF', max_length=14)
    installments = models.IntegerField('Parcelas', default=1)
    response_text = models.TextField(verbose_name='Resposta do provedor', null=True, blank=True)
    pagseguro_url = models.URLField(verbose_name='URL Pagseguro', null=True, blank=True)
    pagseguro_code = models.CharField('Código Pagseguro', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Gerado em', auto_now_add=True)
    paid_at = models.DateTimeField(verbose_name=u'Pago em', null=True, blank=True)

    class Meta:
        verbose_name = u'Pagamento'
        verbose_name_plural = u'Pagamentos Realizados'

    def __unicode__(self):
        return self.payment_key.get_hex()