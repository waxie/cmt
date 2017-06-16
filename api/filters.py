
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
