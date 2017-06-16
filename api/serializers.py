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
    room = serializers.SlugRelatedField(many=False, read_only=False, slug_field='label',
                                        queryset=Room.objects.all())
    contents = serializers.SlugRelatedField(many=True, read_only=True, slug_field='label')

    class Meta:
        model = Rack
        fields = (
            'label', 'capacity', 'room', 'contents', 'url'
        )


class RoomSerializer(DynamicFieldsModelSerializer):
    address = serializers.SlugRelatedField(many=False, read_only=False, slug_field='address',
                                           queryset=Address.objects.all())

    class Meta:
        model = Room
        fields = '__all__'


class AddressSerializer(DynamicFieldsModelSerializer):
    country = serializers.SlugRelatedField(many=False, read_only=False, slug_field='name',
                                           queryset=Country.objects.all())
    rooms = serializers.SlugRelatedField(many=True, read_only=True, slug_field='label')

    class Meta:
        model = Address
        fields = (
            'id', 'address', 'postalcode', 'city', 'note', 'tags',
            'country', 'rooms', 'url'
        )


class CountrySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class RoleSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class ConnectionSerializer(DynamicFieldsModelSerializer):
    company = serializers.SlugRelatedField(many=False, read_only=False, slug_field='name',
                                           queryset=Company.objects.all())
    address = serializers.SlugRelatedField(many=False, read_only=False, slug_field='address',
                                           queryset=Address.objects.all())

    class Meta:
        model = Connection
        fields = '__all__'


class CompanySerializer(DynamicFieldsModelSerializer):
    addresses = serializers.SlugRelatedField(many=True, read_only=True, slug_field='address')

    class Meta:
        model = Company
        fields = '__all__'


class HardwareModelSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = HardwareModel
        fields = '__all__'


class NetworkSerializer(DynamicFieldsModelSerializer):
    interfaces = serializers.SlugRelatedField(many=True, read_only=True, slug_field='api_slug_field')

    class Meta:
        model = Network
        fields = '__all__'


class WarrantyContractSerializer(DynamicFieldsModelSerializer):
    warranty_type = serializers.SlugRelatedField(read_only=False, many=False, slug_field='label',
                                                 queryset=WarrantyType.objects.all())

    class Meta:
        model = WarrantyContract
        fields = '__all__'


class InterfaceSerializer(DynamicFieldsModelSerializer):
    network = serializers.SlugRelatedField(read_only=True, many=False, slug_field='name')
    host = serializers.SlugRelatedField(read_only=True, many=False, slug_field='label')
    iftype = serializers.SlugRelatedField(read_only=True, many=False, slug_field='label')

    class Meta:
        model = Interface


class InterfaceTypeSerializer(DynamicFieldsModelSerializer):
    vendor = serializers.SlugRelatedField(read_only=False, many=False, slug_field='name',
                                          queryset=Company.objects.all())

    class Meta:
        model = InterfaceType
        fields = '__all__'


class WarrantyTypeSerializer(DynamicFieldsModelSerializer):
    contact = serializers.SlugRelatedField(read_only=False, many=False, slug_field='name',
                                              queryset=Connection.objects.all())

    class Meta:
        model = WarrantyType
        fields = '__all__'


class TelephonenumberSerializer(DynamicFieldsModelSerializer):
    country = serializers.SlugRelatedField(read_only=False, many=False, slug_field='name',
                                           queryset=Country.objects.all())
    connection = serializers.SlugRelatedField(read_only=False, many=False, slug_field='name',
                                              queryset=Connection.objects.all())

    class Meta:
        model = Telephonenumber
        fields = '__all__'
