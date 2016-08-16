
import django_filters

from cluster.models import *


class ClusterFilter(django_filters.FilterSet):

    class Meta:
        model = Cluster


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


class RoomFilter(django_filters.FilterSet):

    class Meta:
        model = Room


class AddressFilter(django_filters.FilterSet):
    rooms = django_filters.CharFilter(name="rooms__label")

    class Meta:
        model = Address


class CountryFilter(django_filters.FilterSet):

    class Meta:
        model = Country


class RoleFilter(django_filters.FilterSet):

    class Meta:
        model = Role


class ConnectionFilter(django_filters.FilterSet):

    class Meta:
        model = Connection


class CompanyFilter(django_filters.FilterSet):

    class Meta:
        model = Company


class HardwareModelFilter(django_filters.FilterSet):

    class Meta:
        model = HardwareModel


class NetworkFilter(django_filters.FilterSet):

    class Meta:
        model = Network


class WarrantyContractFilter(django_filters.FilterSet):

    class Meta:
        model = WarrantyContract


class InterfaceFilter(django_filters.FilterSet):

    class Meta:
        model = Interface


class InterfaceTypeFilter(django_filters.FilterSet):

    class Meta:
        model = InterfaceType


class WarrantyTypeFilter(django_filters.FilterSet):

    class Meta:
        model = WarrantyType


class TelephonenumberFilter(django_filters.FilterSet):

    class Meta:
        model = Telephonenumber
