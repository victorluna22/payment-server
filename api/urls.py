from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from rest_framework import routers
from payment.views import PaymentViewSet
from pagseguro import urls as pagseguro_urls

router = routers.DefaultRouter()
router.register(r'payment', PaymentViewSet, 'Payments')

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^retorno/pagseguro/', include(pagseguro_urls))
]


admin.site.site_header = 'Servidor de Pagamento'