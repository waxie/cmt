from django.contrib.auth.models import User, Group
from rest_framework import serializers
from sara_cmt.cluster.models import Cluster, Interface, Network, Rack 
from sara_cmt.cluster.models import HardwareUnit as Equipment
from sara_cmt.cluster.models import Country, Address, Room
from sara_cmt.cluster.models import Company, Connection, Telephonenumber
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyType, WarrantyContract



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name',)


#####
#
# Serializers based on the models in CMT
#


#class ClusterSerializer(serializers.ModelSerializer):
class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cluster
        fields = ('url', 'name', 'machinenames', 'hardware')


#class HardwareSerializer(serializers.ModelSerializer):
class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        #fields = ('url', 'rack', 'first_slot', 'label', 'warranty_tag')
        fields = ('url', 'cluster', 'role', 'network', 'specifications', 'warranty', 'rack', 'seller', 'owner', 'state', 'warranty_tag', 'serial_number', 'first_slot', 'label')


class InterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interface
        fields = ('url', 'network', 'host', 'iftype', 'label', 'aliases', 'hwaddress', 'ip')


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Network
        #fields = ('url', 'name', 'netaddress', 'netmask', 'gateway', 'domain', 'vlan', 'hostnames', 'hardware', 'interfaces')
        fields = ('url', 'name', 'cidr', 'gateway', 'domain', 'vlan', 'hostnames', 'hardware', 'interfaces')


#class RackSerializer(serializers.ModelSerializer):
class RackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rack
        fields = ('url', 'room', 'label', 'capacity', 'contents')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('url', 'name', 'country_code', 'addresses')


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url', 'country', 'address', 'postalcode', 'city')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('url', 'address', 'floor', 'label', 'racks')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('url', 'addresses', 'name', 'website')


class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Connection
        fields = ('url', 'address', 'company', 'active', 'name', 'email', 'sold', 'owns')


class TelephonenumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Telephonenumber
        fields = ('url', 'country', 'connection', 'areacode', 'subscriber_number', 'number_type')


class HardwareModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HardwareModel
        fields = ('url', 'vendor', 'name', 'vendorcode', 'rackspace', 'expansions', 'hardware')


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('url', 'label', 'hardware')


class InterfaceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterfaceType
        fields = ('url', 'vendor', 'label')


class WarrantyTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WarrantyType
        fields = ('url', 'contact', 'label')


class WarrantyContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WarrantyContract
        fields = ('url', 'warranty_type', 'contract_number', 'annual_cost', 'label', 'date_from', 'date_to', 'hardware')
