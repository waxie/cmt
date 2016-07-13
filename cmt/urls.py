
from rest_framework import urls as rest_urls

from api import urls as api_urls
from client import urls as client_urls

from django.conf.urls import include
from django.conf.urls import url

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^api-auth/', include(rest_urls, namespace='rest_framework')),

    url(r'^client/', include(client_urls)),

    ## The Admin urls
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', include(admin.site.urls))
]