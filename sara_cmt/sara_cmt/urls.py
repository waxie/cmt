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

from django.conf.urls.defaults import include, patterns, url
from django.contrib import databrowse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^core/', include('core.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^db/(.*)', databrowse.site.root),

    # !!! Multiple admin-sites !!!
    #  http://docs.djangoproject.com/en/dev/ref/contrib/admin/#multiple-admin-sites-in-the-same-urlconf
)

# core
from sara_cmt.cluster.models import Cluster, HardwareUnit, Interface, \
                                    Network, Rack
databrowse.site.register(Cluster)
databrowse.site.register(HardwareUnit)
databrowse.site.register(Interface)
databrowse.site.register(Network)
databrowse.site.register(Rack)
# locations
from sara_cmt.cluster.models import Country, Address, Room
databrowse.site.register(Country)
databrowse.site.register(Address)
databrowse.site.register(Room)
# contacts
from sara_cmt.cluster.models import Company, Telephonenumber, Connection
databrowse.site.register(Company)
databrowse.site.register(Telephonenumber)
databrowse.site.register(Connection)
# specifications
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
databrowse.site.register(HardwareModel)
databrowse.site.register(Role)
databrowse.site.register(InterfaceType)
# support
from sara_cmt.cluster.models import WarrantyContract, WarrantyType
databrowse.site.register(WarrantyContract)
databrowse.site.register(WarrantyType)

# tags
from tagging.models import *
databrowse.site.register(Tag)
databrowse.site.register(TaggedItem)
