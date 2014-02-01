
from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.models import User, Group
from rest_framework import routers
#from django.core.urlresolvers import reverse
from cmt_server.apps.api.views import *

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()


## locations of equipment in a cluster
router.register(r'cluster', ClusterViewSet)
router.register(r'hardwareunit', EquipmentViewSet)
router.register(r'racks', RackViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'countries', CountryViewSet) # not really necessary
router.register(r'rooms', RoomViewSet)

## network-related info of equipment
router.register(r'interfaces', InterfaceViewSet)
router.register(r'networks', NetworkViewSet)

## contact-related info of relations
router.register(r'contacts', ConnectionViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'telephonenumbers', TelephonenumberViewSet)

## equipment-related info
router.register(r'hardwaremodels', HardwareModelViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'interfacetypes', InterfaceTypeViewSet)

## warranty-related info
router.register(r'warrantytypes', WarrantyTypeViewSet)
router.register(r'warrantycontracts', WarrantyContractViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Examples:
    # url(r'^$', 'cmt_server.views.home', name='home'),
    # url(r'^cmt_server/', include('cmt_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
