#
# This file is part of CMT
#
# CMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# CMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMT.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2017 SURFsara

# Django core
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView


## Django third party
from rest_framework import urls as rest_urls

## cmt
from api import urls as api_urls
from client import urls as client_urls

admin.autodiscover()



urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^api-auth/', include(rest_urls, namespace='rest_framework')),

    url(r'^client/', include(client_urls)),

    ## The Admin urls
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/admin', permanent=True), name='go-to-admin'),
]
