# -*- coding: utf-8 -*-
import uuid
from django.db import models
from .providers.cielo_provider import pay_cielo_test, pay_cielo, authorize_cielo, confirm_cielo
from .providers.redecard_provider import pay_redecard_test, pay_redecard, authorize_redecard, confirm_redecard
from .providers.pagseguro_provider import pay_pagseguro_test, pay_pagseguro
from .providers.paypal_provider import pay_paypal_test

CIELO, REDECARD, PAGSEGURO, PAYPAL = 'cielo', 'redecard', 'pagseguro', 'paypal'


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

    def authorize(self, data, payment):
        if self.slug == CIELO:
            return authorize_cielo(data, payment)
        elif self.slug == REDECARD:
            return authorize_redecard(data, payment)

    def confirm(self, payment):
        if self.slug == CIELO:
            return confirm_cielo(payment)
        elif self.slug == REDECARD:
            return confirm_redecard(payment)

    def pay(self, data, payment):
        if self.slug == CIELO:
            return pay_cielo(data, payment)
        elif self.slug == REDECARD:
            return pay_redecard(data, payment)
        elif self.slug == PAGSEGURO:
            return pay_pagseguro(data, payment)
        elif self.slug == PAYPAL:
            return pay_paypal_test(data, payment)

    def pay_test(self, data, payment):
        if self.slug == CIELO:
            return pay_cielo_test(data, payment)
        elif self.slug == REDECARD:
            return pay_redecard_test(data, payment)
        elif self.slug == PAGSEGURO:
            return pay_pagseguro(data, payment)
        elif self.slug == PAYPAL:
            return pay_paypal_test(data, payment)


class TargetProvider(models.Model):
    provider = models.ForeignKey(PaymentProvider, verbose_name='Provedor')
    updated_at = models.DateTimeField(verbose_name='Última atualização', auto_now=True)

    class Meta:
        verbose_name = u'Chavear Provedor'
        verbose_name_plural = u'Chavear Provedor'

    def __unicode__(self):
        return self.provider.name


VISA, MASTERCARD, DINERS, DISCOVER, ELO, AMEX, JCB, AURA = 'visa', 'mastercard', 'diners', 'discover', 'elo', 'amex', 'JCB', 'Aura'
CARD_TYPES = (
    (VISA, 'Visa'),
    (MASTERCARD, 'Mastercard'),
    (DINERS, 'Diners'),
    (DISCOVER, 'Discover'),
    (ELO, 'Elo'),
    (AMEX, 'Amex'),
    (JCB, 'JCB'),
    (AURA, 'Aura'),
)


class Payment(models.Model):
    payment_key = models.UUIDField(verbose_name='Chave de pagamento', max_length=64, default=uuid.uuid4, editable=False, unique=True)
    provider = models.ForeignKey(PaymentProvider, verbose_name='Provedor')
    value = models.DecimalField(u'Valor', max_digits=9, decimal_places=2, default=0)
    status_code = models.IntegerField('Cod', null=True, blank=True, db_index=True)
    name = models.CharField('Nome', max_length=100)
    project = models.SlugField('Projeto', null=True, blank=True)
    card_type = models.CharField('Bandeira', max_length=30, choices=CARD_TYPES)
    cpf = models.CharField('CPF', max_length=14)
    installments = models.IntegerField('Parcelas', default=1)
    response_text = models.TextField(verbose_name='Resposta do provedor', null=True, blank=True)
    numcv = models.CharField('Comprovante de vendas Rede', max_length=100, null=True, blank=True)
    numautor = models.CharField('Número Autorização Rede', max_length=100, null=True, blank=True)
    tid = models.CharField('Transação ID Cielo', max_length=100, null=True, blank=True)
    pagseguro_url = models.URLField(verbose_name='URL Pagseguro', null=True, blank=True)
    pagseguro_code = models.CharField('Código Pagseguro', max_length=255, null=True, blank=True)
    paypal_code = models.CharField('Código Paypal', max_length=255)
    is_authorized = models.BooleanField('Aut.', default=0)
    is_paid = models.BooleanField('Pago', default=0)
    created_at = models.DateTimeField(verbose_name='Gerado em', auto_now_add=True)
    paid_at = models.DateTimeField(verbose_name=u'Pago em', null=True, blank=True)

    class Meta:
        verbose_name = u'Pagamento'
        verbose_name_plural = u'Pagamentos Realizados'

    def __unicode__(self):
        return self.payment_key.get_hex()