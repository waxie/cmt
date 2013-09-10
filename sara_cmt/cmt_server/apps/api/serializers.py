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


class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')

    class Meta:
        model = Cluster


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    interfaces = serializers.HyperlinkedRelatedField(many=True, view_name='interface-detail')

    class Meta:
        model = Equipment
        depth = 1


class InterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interface
        depth = 1


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')
    interfaces = serializers.HyperlinkedRelatedField(many=True, view_name='interface-detail')

    class Meta:
        model = Network


class RackSerializer(serializers.HyperlinkedModelSerializer):
    contents = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')

    class Meta:
        model = Rack


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    rooms = serializers.HyperlinkedRelatedField(many=True, view_name='room-detail')

    class Meta:
        model = Address


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    racks = serializers.HyperlinkedRelatedField(many=True, view_name='rack-detail')

    class Meta:
        model = Room


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company


class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Connection


class TelephonenumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Telephonenumber


class HardwareModelSerializer(serializers.HyperlinkedModelSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')

    class Meta:
        model = HardwareModel


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role


class InterfaceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterfaceType


class WarrantyTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WarrantyType


class WarrantyContractSerializer(serializers.HyperlinkedModelSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')

    class Meta:
        model = WarrantyContract

#
#
#####
