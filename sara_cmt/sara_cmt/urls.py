#    This file is part of CMT, a Cluster Management Tool made at SURFsara.
#    Copyright (C) 2012, 2013  Sil Westerveld, Ramon Bastiaans
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from django.conf.urls import include, patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^core/', include('core.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS

    url(r'^admin/', include('smuggler.urls')), # put it before admin url patterns

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # !!! Multiple admin-sites !!!
    #  http://docs.djangoproject.com/en/dev/ref/contrib/admin/#multiple-admin-sites-in-the-same-urlconf
)
