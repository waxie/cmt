### Create your views here.
##
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters

from sara_cmt.cluster.models import Cluster, Rack, Room, Address, Country
from sara_cmt.cluster.models import HardwareUnit as Equipment
from sara_cmt.cluster.models import Interface, Network
from sara_cmt.cluster.models import Connection, Company, Telephonenumber
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyType, WarrantyContract

from cmt_server.apps.api.serializers import ClusterSerializer, EquipmentSerializer, RackSerializer, RoomSerializer, AddressSerializer, CountrySerializer
from cmt_server.apps.api.serializers import InterfaceSerializer, NetworkSerializer
from cmt_server.apps.api.serializers import ConnectionSerializer, CompanySerializer, TelephonenumberSerializer
from cmt_server.apps.api.serializers import HardwareModelSerializer, RoleSerializer, InterfaceTypeSerializer
from cmt_server.apps.api.serializers import WarrantyTypeSerializer, WarrantyContractSerializer


#class UserViewSet(viewsets.ModelViewSet):
#    """
#    Returns a list of **all** registered users.
#    
#    For more details about the user please [see here][ref].
#
#    [ref]: https://intranet.surfsara.nl/algemeen/wiki/Telefoonlijst
#    """
#    model = User
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

#class GroupViewSet(viewsets.ModelViewSet):
#    model = Group
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer
#


#####
#
# Viewsets based on the models in CMT. They define the view behavior.
#

# Equipment-related
class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    fields = ('url',)
    filter_fields = ('name',)
    # model = Cluster
    # lookup_fields = (...

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_fields = (
            'cluster__name', 'role__label', 'network__name', 'network__vlan',
            'specifications__name', 'warranty__label', 'warranty__contract_number',
            'rack__label', 'warranty_tag', 'serial_number', 'first_slot', 'label',
            #'in_support'
            )


class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    filter_fields = ('label', 'room__label')

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('label', 'address__address')

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_fields = (
            'country__name', 'country__country_code', 'address'
            'postalcode', 'city'
            )

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_fields = ('name', 'country_code')


# Network-related
class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    filter_fields = (
            'network__name', 'network__vlan', 'host__label', 'iftype__label',
            'label', 'aliases', 'hwaddress', 'ip'
            )

class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_fields = (
            'name', 'cidr', 'gateway', 'domain', 'vlan'
            )


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filter_fields = ('name',)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_fields = ('name',)


class TelephonenumberViewSet(viewsets.ModelViewSet):
    queryset = Telephonenumber.objects.all()
    serializer_class = TelephonenumberSerializer
    filter_fields = ('connection__name',)


class HardwareModelViewSet(viewsets.ModelViewSet):
    queryset = HardwareModel.objects.all()
    serializer_class = HardwareModelSerializer
    filter_fields = ('vendor__name', 'name', 'vendorcode')


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_fields = ('label',)


class InterfaceTypeViewSet(viewsets.ModelViewSet):
    queryset = InterfaceType.objects.all()
    serializer_class = InterfaceTypeSerializer
    filter_fields = ('vendor__name', 'label')


class WarrantyTypeViewSet(viewsets.ModelViewSet):
    queryset = WarrantyType.objects.all()
    serializer_class = WarrantyTypeSerializer
    filter_fields = ('contact__name', 'label')


class WarrantyContractViewSet(viewsets.ModelViewSet):
    queryset = WarrantyContract.objects.all()
    serializer_class = WarrantyContractSerializer
    filter_fields = ('warranty_type__label', 'contract_number', 'label')
