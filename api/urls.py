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

from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from api.views import *

router_v2 = routers.DefaultRouter(trailing_slash=False)

router_v2.register(r'cluster', ClusterViewSet)
router_v2.register(r'equipment', EquipmentViewSet)
router_v2.register(r'rack', RackViewSet)
router_v2.register(r'room', RoomViewSet)
router_v2.register(r'address', AddressViewSet)
router_v2.register(r'country', CountryViewSet)
router_v2.register(r'role', RoleViewSet)
router_v2.register(r'connection', ConnectionViewSet)
router_v2.register(r'company', CompanyViewSet)
router_v2.register(r'hardwaremodel', HardwareModelViewSet)
router_v2.register(r'network', NetworkViewSet)
router_v2.register(r'warrantycontract', WarrantyContractViewSet)
router_v2.register(r'interface', InterfaceViewSet)
router_v2.register(r'interfacetype', InterfaceTypeViewSet)
router_v2.register(r'warrantytype', WarrantyTypeViewSet)
router_v2.register(r'telephonenumber', TelephonenumberViewSet)

urlpatterns = [
    url(r'^v2/template', TemplateView.as_view() ),
    url(r'^v2/', include(router_v2.urls), name='api-v2'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
