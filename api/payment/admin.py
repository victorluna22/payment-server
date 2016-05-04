from django.contrib import admin
from .models import PaymentProvider, Payment, TargetProvider


class PaymentProviderAdmin(admin.ModelAdmin):
     model = PaymentProvider
     list_display = ('id', 'name', 'slug', 'status')

     # def has_add_permission(self, request):
     #     return False
     #
     # def has_delete_permission(self, request, obj=None):
     #     return False


class TargetProviderAdmin(admin.ModelAdmin):
    model = TargetProvider
    list_display = ('provider', 'updated_at', 'acao')
    list_display_links = ('acao', )

    def acao(self, obj):
        return 'mudar'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    readonly_fields = Payment._meta.get_all_field_names()
    list_display = ('payment_key', 'name', 'value', 'card_type', 'provider', 'status_code', 'created_at', 'paid_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(TargetProvider, TargetProviderAdmin)