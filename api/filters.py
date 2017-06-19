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

import django_filters

from cluster.models import *


class ClusterFilter(django_filters.FilterSet):

    class Meta:
        model = Cluster
        fields = '__all__'


class EquipmentFilter(django_filters.FilterSet):

    cluster = django_filters.CharFilter(name="cluster__name")
    rack = django_filters.CharFilter(name="rack__label")
    network = django_filters.CharFilter(name="network__name")
    specifications = django_filters.CharFilter(name="specifications__name")
    warranty = django_filters.CharFilter(name="warranty__label")
    seller = django_filters.CharFilter(name="seller__name")
    owner = django_filters.CharFilter(name="owner__name")

    class Meta:
        model = Equipment
        fields = [
            'cluster', 'rack', 'network', 'specifications', 'warranty', 'seller', 'owner',
            'state', 'warranty_tag', 'serial_number', 'first_slot', 'label'
        ]


class RackFilter(django_filters.FilterSet):
    room = django_filters.CharFilter(name="room__label")

    class Meta:
        model = Rack
        fields = '__all__'


class RoomFilter(django_filters.FilterSet):

    class Meta:
        model = Room
        fields = '__all__'


class AddressFilter(django_filters.FilterSet):
    rooms = django_filters.CharFilter(name="rooms__label")

    class Meta:
        model = Address
        fields = '__all__'


class CountryFilter(django_filters.FilterSet):

    class Meta:
        model = Country
        fields = '__all__'


class RoleFilter(django_filters.FilterSet):

    class Meta:
        model = Role
        fields = '__all__'


class ConnectionFilter(django_filters.FilterSet):

    class Meta:
        model = Connection
        fields = '__all__'


class CompanyFilter(django_filters.FilterSet):

    class Meta:
        model = Company
        fields = '__all__'


class HardwareModelFilter(django_filters.FilterSet):

    class Meta:
        model = HardwareModel
        fields = '__all__'


class NetworkFilter(django_filters.FilterSet):

    class Meta:
        model = Network
        fields = '__all__'


class WarrantyContractFilter(django_filters.FilterSet):

    class Meta:
        model = WarrantyContract
        fields = '__all__'


class InterfaceFilter(django_filters.FilterSet):

    class Meta:
        model = Interface
        fields = '__all__'


class InterfaceTypeFilter(django_filters.FilterSet):

    class Meta:
        model = InterfaceType
        fields = '__all__'


class WarrantyTypeFilter(django_filters.FilterSet):

    class Meta:
        model = WarrantyType
        fields = '__all__'


class TelephonenumberFilter(django_filters.FilterSet):

    class Meta:
        model = Telephonenumber
        fields = '__all__'
