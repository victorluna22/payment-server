from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
