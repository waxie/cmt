
from cluster.models import *
from api import fields

from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        if 'context' in kwargs:
            field_args = kwargs['context'].pop('fields', None)
        else:
            field_args = None

        if field_args:
            fields = field_args.split(',')
        else:
            fields = None

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ClusterSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Cluster
        fields = (
            'url', 'name', 'machinenames', 'hardware'
        )


class EquipmentSerializer(DynamicFieldsModelSerializer):
    cluster = fields.BasicField(read_only=False, many=False)
    rack = serializers.SlugRelatedField(read_only=True, many=False, slug_field='label')
    role = serializers.SlugRelatedField(read_only=True, many=True, slug_field='label')
    seller = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')
    owner = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')
    specifications = serializers.SlugRelatedField(read_only=True, many=False, slug_field='api_slug_field')
    interfaces = serializers.SlugRelatedField(read_only=True, many=True, slug_field='api_slug_field')
    warranty = serializers.SlugRelatedField(read_only=True, many=False, slug_field='api_slug_field')

    class Meta:
        model = Equipment
        fields = (
            'state', 'warranty_tag', 'serial_number', 'first_slot', 'label', 'note', 'updated_on', 'created_on', 'url',
            'cluster', 'rack', 'role', 'seller', 'owner', 'specifications', 'interfaces', 'warranty'
        )


class RackSerializer(DynamicFieldsModelSerializer):
    room = serializers.SlugRelatedField(many=False, read_only=True, slug_field='label')
    contents = serializers.SlugRelatedField(many=True, read_only=True, slug_field='label')

    class Meta:
        model = Rack
        fields = (
            'label', 'capacity',
            'room', 'contents'
        )


class RoomSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Room


class AddressSerializer(DynamicFieldsModelSerializer):
    country = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    rooms = serializers.SlugRelatedField(many=True, read_only=True, slug_field='label')

    class Meta:
        model = Address
        fields = (
            'address', 'postalcode', 'city', 'note', 'tags',
            'country', 'rooms'
        )


class CountrySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Country


class RoleSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Role


class ConnectionSerializer(DynamicFieldsModelSerializer):
    company = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    address = serializers.SlugRelatedField(many=False, read_only=True, slug_field='address')

    class Meta:
        model = Connection


class CompanySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Company


class HardwareModelSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = HardwareModel


class NetworkSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Network


class WarrantyContractSerializer(DynamicFieldsModelSerializer):
    warranty_type = serializers.SlugRelatedField(read_only=True, many=False, slug_field='label')

    class Meta:
        model = WarrantyContract


class InterfaceSerializer(DynamicFieldsModelSerializer):
    network = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')
    host = serializers.SlugRelatedField(read_only=True, many=False, slug_field='label')
    iftype = serializers.SlugRelatedField(read_only=True, many=False, slug_field='label')

    class Meta:
        model = Interface


class InterfaceTypeSerializer(DynamicFieldsModelSerializer):
    vendor = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')

    class Meta:
        model = InterfaceType


class WarrantyTypeSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = WarrantyType


class TelephonenumberSerializer(DynamicFieldsModelSerializer):
    country = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')
    connection = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')

    class Meta:
        model = Telephonenumber
