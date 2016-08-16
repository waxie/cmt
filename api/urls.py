
from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from api.views import *

router_v1 = routers.DefaultRouter(trailing_slash=False)

router_v1.register(r'cluster', ClusterViewSet)
router_v1.register(r'equipment', EquipmentViewSet)
router_v1.register(r'rack', RackViewSet)
router_v1.register(r'room', RoomViewSet)
router_v1.register(r'address', AddressViewSet)
router_v1.register(r'country', CountryViewSet)
router_v1.register(r'role', RoleViewSet)
router_v1.register(r'connection', ConnectionViewSet)
router_v1.register(r'company', CompanyViewSet)
router_v1.register(r'hardwaremodel', HardwareModelViewSet)
router_v1.register(r'network', NetworkViewSet)
router_v1.register(r'warrantycontract', WarrantyContractViewSet)
router_v1.register(r'interface', InterfaceViewSet)
router_v1.register(r'interfacetype', InterfaceTypeViewSet)
router_v1.register(r'warrantytype', WarrantyTypeViewSet)
router_v1.register(r'telephonenumber', TelephonenumberViewSet)

# Old naming support :(
#router_v1.register(r'clusters', ClusterViewSet)
#router_v1.register(r'racks', RackViewSet)
#router_v1.register(r'rooms', RoomViewSet)
#router_v1.register(r'addresses', AddressViewSet)
#router_v1.register(r'countries', CountryViewSet)
#router_v1.register(r'roles', RoleViewSet)
#router_v1.register(r'contacts', ConnectionViewSet)
#router_v1.register(r'companies', CompanyViewSet)
#router_v1.register(r'hardwaremodels', HardwareModelViewSet)
#router_v1.register(r'networks', NetworkViewSet)
#router_v1.register(r'warrantycontracts', WarrantyContractViewSet)

urlpatterns = [
    url(r'^v1/template', TemplateView.as_view() ),
    url(r'^v1/', include(router_v1.urls), name='api-v1'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
