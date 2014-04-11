
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers

from cmt_server.apps.api.views import *

# Routers provide an easy way of automatically determining the URL conf
router_v1 = routers.DefaultRouter()

## locations of equipment in a cluster
router_v1.register(r'clusters', ClusterViewSet)
router_v1.register(r'equipment', EquipmentViewSet)
router_v1.register(r'racks', RackViewSet)
router_v1.register(r'addresses', AddressViewSet)
router_v1.register(r'countries', CountryViewSet) # not really necessary
router_v1.register(r'rooms', RoomViewSet)

## network-related info of equipment
router_v1.register(r'interfaces', InterfaceViewSet)
router_v1.register(r'networks', NetworkViewSet)

## contact-related info of relations
router_v1.register(r'contacts', ConnectionViewSet)
router_v1.register(r'companies', CompanyViewSet)
router_v1.register(r'telephonenumbers', TelephonenumberViewSet)

## equipment-related info
router_v1.register(r'hardwaremodels', HardwareModelViewSet)
router_v1.register(r'roles', RoleViewSet)
router_v1.register(r'interfacetypes', InterfaceTypeViewSet)

## warranty-related info
router_v1.register(r'warrantytypes', WarrantyTypeViewSet)
router_v1.register(r'warrantycontracts', WarrantyContractViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^api/v1/template', TemplateView.as_view() ),
    url(r'^api/v1/', include(router_v1.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Examples:
    # url(r'^$', 'cmt_server.views.home', name='home'),
    # url(r'^cmt_server/', include('cmt_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS

    url(r'^admin/', include('smuggler.urls')), # put it before admin url patterns

    url(r'^admin/', include(admin.site.urls))
)