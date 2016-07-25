# vim: set noai tabstop=4 shiftwidth=4 expandtab:

from rest_framework import serializers

from cluster.models import *

#####
#
# Serializers based on the models in CMT
#

class CMTSerializer(serializers.HyperlinkedModelSerializer):

    def __init__(self, *args, **kwargs):

        #RB: based upon http://www.django-rest-framework.org/api-guide/serializers.html#dynamically-modifying-fields

        # Get the fields args from extra supplied context
        fields_args = kwargs['context'].pop('fields', None)

        fields = None

        if fields_args:

            fields = fields_args.split(',')

        # Instantiate the superclass normally
        super(CMTSerializer, self).__init__(*args, **kwargs)

        if fields:

            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                print 'popping ' + field_name

class ClusterSerializer(CMTSerializer):
    hardware = serializers.HyperlinkedRelatedField(many=True, view_name='equipment-detail', required=False)
    #equipments = django.db.models.ForeignKey(Equipment, related_name='cluster')

    class Meta:
        model = Cluster
        #fields = ('url', 'name', 'hardware')

class InterfaceListingField(serializers.RelatedField):
    def to_native(self, value):

        return '%s : %s (%s)' %(value.label, value.network.name, value.iftype)


class EquipmentSerializer(CMTSerializer):
    cluster = serializers.SlugRelatedField(required=True, many=False, read_only=False, slug_field='name')
    rack = serializers.SlugRelatedField(required=True, many=False, read_only=False, slug_field='label')
    interfaces = InterfaceListingField(many=True)
    role = serializers.SlugRelatedField(required=False, many=True, read_only=False, slug_field='label' )
    specifications = serializers.SlugRelatedField(required=False, many=False, read_only=False, slug_field='name')
    warranty = serializers.SlugRelatedField(required=False, many=False, read_only=False, slug_field='label')
    seller = serializers.SlugRelatedField(required=False, many=False, read_only=False, slug_field='name')
    owner = serializers.SlugRelatedField(required=False, many=False, read_only=False, slug_field='name')

    class Meta:
        model = Equipment
        fields = ( 'cluster', 'created_on', 'first_slot', 'interfaces', 'label', 'note', 'owner', 'rack',
               'role', 'seller', 'owner', 'serial_number', 'specifications', 'state', 'updated_on', 'url',
               'warranty', 'warranty_tag' )
        #depth = 1


class RackSerializer(CMTSerializer):
    #contents = serializers.HyperlinkedRelatedField(many=True, view_name='equipment-detail')
    room = serializers.RelatedField( many=False )

    class Meta:
        model = Rack


class AddressSerializer(CMTSerializer):
    #rooms = serializers.HyperlinkedRelatedField(many=True, view_name='room-detail')
    country = serializers.RelatedField( many=False )

    class Meta:
        model = Address


class CountrySerializer(CMTSerializer):
    #addresses = serializers.HyperlinkedRelatedField(many=True, view_name='address-detail')

    class Meta:
        model = Country

class AddressListingField(serializers.RelatedField):
    def to_native(self, value):

        return '%s, %s (%s)' %(value.address, value.city, value.country.name)

class RoomSerializer(CMTSerializer):
    #racks = serializers.HyperlinkedRelatedField(many=True, view_name='rack-detail')
    address = AddressListingField( many=False )

    class Meta:
        model = Room


class InterfaceSerializer(CMTSerializer):
    host = serializers.SlugRelatedField(required=True, many=False, read_only=False, slug_field='label')
    iftype = serializers.SlugRelatedField(required=True, many=False, read_only=False, slug_field='label')
    network = serializers.SlugRelatedField(required=True, many=False, read_only=False, slug_field='name')
    fqdn = serializers.CharField(source='fqdn', required=False, read_only=True)

    class Meta:
        model = Interface
        #depth = 1


class NetworkSerializer(CMTSerializer):
    #hardware = serializers.HyperlinkedRelatedField(many=True, view_name='equipment-detail')
    #interfaces = serializers.HyperlinkedRelatedField(many=True, view_name='interface-detail')
    netaddress = serializers.CharField(source='netaddress')
    netmask    = serializers.CharField(source='netmask')

    class Meta:
        model = Network


class ConnectionSerializer(CMTSerializer):
    address = AddressListingField( many=False )
    company = serializers.RelatedField( many=False )
    
    class Meta:
        model = Connection


class CompanySerializer(CMTSerializer):
    addresses = AddressListingField( many=True )

    class Meta:
        model = Company


class TelephonenumberSerializer(CMTSerializer):
    connection = serializers.RelatedField( many=False )
    country = serializers.RelatedField( many=False )

    class Meta:
        model = Telephonenumber


class HardwareModelSerializer(CMTSerializer):
    #hardware = serializers.HyperlinkedRelatedField(many=True, view_name='equipment-detail')
    vendor = serializers.RelatedField( many=False )

    class Meta:
        model = HardwareModel


class RoleSerializer(CMTSerializer):
    class Meta:
        model = Role

class InterfaceTypeSerializer(CMTSerializer):
    vendor = serializers.RelatedField( many=False )

    class Meta:
        model = InterfaceType


class WarrantyTypeSerializer(CMTSerializer):
    contact = serializers.RelatedField( many=False )

    class Meta:
        model = WarrantyType


class WarrantyContractSerializer(CMTSerializer):
    #hardware = serializers.HyperlinkedRelatedField(many=True, view_name='equipment-detail')

    warranty_type = serializers.RelatedField( many=False )

    class Meta:
        model = WarrantyContract

#
#
#####
