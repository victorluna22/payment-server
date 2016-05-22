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
    list_filter = ('provider', 'is_authorized', 'is_paid', 'project')
    search_fields = ['payment_key', 'name']
    list_display = ('payment_key', 'project', 'value', 'provider', 'status_code', 'is_authorized', 'is_paid', 'created_format', 'paid_format')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def created_format(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M") if obj.created_at else None
    created_format.short_description = 'Gerado em'

    def paid_format(self, obj):
        return obj.paid_at.strftime("%d/%m/%Y %H:%M") if obj.paid_at else None
    paid_format.short_description = 'Pago em'


admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(TargetProvider, TargetProviderAdmin)