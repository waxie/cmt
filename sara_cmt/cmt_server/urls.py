from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from django.core.urlresolvers import reverse
from sara_cmt.cluster.models import Cluster, Interface, Network, Rack 
from sara_cmt.cluster.models import HardwareUnit as Equipment
from sara_cmt.cluster.models import Country, Address, Room
from sara_cmt.cluster.models import Company, Connection, Telephonenumber
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyType, WarrantyContract

from cmt_server.apps.api.serializers import UserSerializer, GroupSerializer, ClusterSerializer, EquipmentSerializer, InterfaceSerializer, NetworkSerializer, RackSerializer
from cmt_server.apps.api.serializers import CountrySerializer, AddressSerializer, RoomSerializer
from cmt_server.apps.api.serializers import CompanySerializer, ConnectionSerializer, TelephonenumberSerializer
from cmt_server.apps.api.serializers import HardwareModelSerializer, RoleSerializer, InterfaceTypeSerializer
from cmt_server.apps.api.serializers import WarrantyTypeSerializer, WarrantyContractSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """
    Returns a list of **all** registered users.
    
    For more details about the user please [see here][ref].

    [ref]: https://intranet.surfsara.nl/algemeen/wiki/Telefoonlijst
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    model = Group
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    model = Cluster
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    model = Equipment
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class InterfaceViewSet(viewsets.ModelViewSet):
    model = Interface
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    model = Network
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class RackViewSet(viewsets.ModelViewSet):
    model = Rack
    queryset = Rack.objects.all()
    serializer_class = RackSerializer


class CountryViewSet(viewsets.ModelViewSet):
    model = Country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AddressViewSet(viewsets.ModelViewSet):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class RoomViewSet(viewsets.ModelViewSet):
    model = Room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ConnectionViewSet(viewsets.ModelViewSet):
    model = Connection
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class TelephonenumberViewSet(viewsets.ModelViewSet):
    model = Telephonenumber
    queryset = Telephonenumber.objects.all()
    serializer_class = TelephonenumberSerializer


class HardwareModelViewSet(viewsets.ModelViewSet):
    model = HardwareModel
    queryset = HardwareModel.objects.all()
    serializer_class = HardwareModelSerializer


class RoleViewSet(viewsets.ModelViewSet):
    model = Role
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class InterfaceTypeViewSet(viewsets.ModelViewSet):
    model = InterfaceType
    queryset = InterfaceType.objects.all()
    serializer_class = InterfaceTypeSerializer


class WarrantyTypeViewSet(viewsets.ModelViewSet):
    model = WarrantyType
    queryset = WarrantyType.objects.all()
    serializer_class = WarrantyTypeSerializer


class WarrantyContractViewSet(viewsets.ModelViewSet):
    model = WarrantyContract
    queryset = WarrantyContract.objects.all()
    serializer_class = WarrantyContractSerializer


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'interfaces', InterfaceViewSet)
router.register(r'networks', NetworkViewSet)
router.register(r'racks', RackViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'contacts', ConnectionViewSet)
router.register(r'telephonenumbers', TelephonenumberViewSet)
router.register(r'hardwaremodels', HardwareModelViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'interfacetypes', InterfaceTypeViewSet)
router.register(r'warrantytypes', WarrantyTypeViewSet)
router.register(r'warrantycontracts', WarrantyContractViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    # Examples:
    # url(r'^$', 'cmt_server.views.home', name='home'),
    # url(r'^cmt_server/', include('cmt_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
