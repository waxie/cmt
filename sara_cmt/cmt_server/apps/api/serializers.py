##from django.contrib.auth.models import User, Group
from rest_framework import serializers

from sara_cmt.cluster.models import Cluster, Interface, Network, Rack, Room, Address, Country
from sara_cmt.cluster.models import HardwareUnit as Equipment
from sara_cmt.cluster.models import Interface, Network
from sara_cmt.cluster.models import Connection, Company, Telephonenumber
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyType, WarrantyContract


#####
#
# Serializers based on the models in CMT
#

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail', required=False)

    class Meta:
        model = Cluster
        #fields = ('url', 'name', 'hardware')


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    cluster = serializers.HyperlinkedRelatedField(many=False, view_name='cluster-detail')
    interfaces = serializers.HyperlinkedRelatedField(many=True, view_name='interface-detail')

    class Meta:
        model = Equipment
        #fields = ('cluster', 'rack', 'first_slot', 'label')
        #depth = 1


class RackSerializer(serializers.HyperlinkedModelSerializer):
    contents = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')

    class Meta:
        model = Rack


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    rooms = serializers.HyperlinkedRelatedField(many=True, view_name='room-detail')

    class Meta:
        model = Address


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    addresses = serializers.HyperlinkedRelatedField(many=True, view_name='address-detail')

    class Meta:
        model = Country


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    racks = serializers.HyperlinkedRelatedField(many=True, view_name='rack-detail')

    class Meta:
        model = Room


class InterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interface
        #depth = 1


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='hardwareunit-detail')
    interfaces = serializers.HyperlinkedRelatedField(many=True, view_name='interface-detail')

    class Meta:
        model = Network


class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Connection


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company


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
