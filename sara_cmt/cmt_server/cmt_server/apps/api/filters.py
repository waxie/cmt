
import django_filters
from cmt_server.apps.cluster.models import HardwareUnit as Equipment
from cmt_server.apps.cluster.models import Rack, Room, Interface, Address, Connection, Company, Telephonenumber
from cmt_server.apps.cluster.models import HardwareModel, InterfaceType, WarrantyType, WarrantyContract

class EquipmentFilter(django_filters.FilterSet):

    cluster        = django_filters.CharFilter(name="cluster__name")
    rack           = django_filters.CharFilter(name="rack__label")
    network        = django_filters.CharFilter(name="network__name")
    specifications = django_filters.CharFilter(name="specifications__name")
    warranty       = django_filters.CharFilter(name="warranty__label")
    seller         = django_filters.CharFilter(name="seller__name")
    owner          = django_filters.CharFilter(name="owner__name")

    class Meta:
        model = Equipment

        fields =  [
            'cluster', 'rack', 'network', 'specifications', 'warranty', 'seller', 'owner',
            'state', 'warranty_tag', 'serial_number', 'first_slot', 'label'
            ]

        order_by = 'label'

class RackFilter(django_filters.FilterSet):

    room          = django_filters.CharFilter(name="room__label")

    class Meta:
        model = Rack

        fields =  [ 'room', 'label', 'capacity' ]

class RoomFilter(django_filters.FilterSet):

    address       = django_filters.CharFilter(name="address__address")

    class Meta:
        model = Room

        fields =  [ 'address', 'floor', 'label' ]

class AddressFilter(django_filters.FilterSet):

    country       = django_filters.CharFilter(name="country__name")

    class Meta:
        model = Address

        fields =  [ 'country', 'address', 'postalcode', 'city' ]

class InterfaceFilter(django_filters.FilterSet):

    network = django_filters.CharFilter(name="network__name")
    host    = django_filters.CharFilter(name="equipment__label")
    iftype  = django_filters.CharFilter(name="iftype__label")

    class Meta:
        model = Interface

        fields =  [ 'network', 'host', 'iftype', 'label', 'aliases', 'hwaddress', 'ip' ]

class ConnectionFilter(django_filters.FilterSet):

    address       = django_filters.CharFilter(name="address__address")
    company       = django_filters.CharFilter(name="company__name")

    class Meta:
        model = Connection

        fields =  [ 'address', 'company', 'active', 'name', 'email' ]

class CompanyFilter(django_filters.FilterSet):

    addresses    = django_filters.CharFilter(name="address__address")

    class Meta:
        model = Company

        fields =  [ 'addresses', 'name', 'website' ]

class TelephonenumberFilter(django_filters.FilterSet):

    country       = django_filters.CharFilter(name="country__name")
    connection    = django_filters.CharFilter(name="connection__name")

    class Meta:
        model = Telephonenumber

        fields =  [ 'country', 'connection', 'areacode', 'subscriber_number', 'number_type' ]

class HardwareModelFilter(django_filters.FilterSet):

    vendor = django_filters.CharFilter(name="vendor__name")

    class Meta:
        model = HardwareModel

        fields =  [ 'vendor', 'name', 'vendorcode', 'rackspace', 'expansions' ]


class InterfaceTypeFilter(django_filters.FilterSet):

    vendor = django_filters.CharFilter(name="vendor__name")

    class Meta:
        model = InterfaceType

        fields =  [ 'vendor', 'label' ]

class WarrantyTypeFilter(django_filters.FilterSet):

    contact = django_filters.CharFilter(name="contact__name")

    class Meta:
        model = WarrantyType

        fields =  [ 'contact', 'label' ]

class WarrantyContractFilter(django_filters.FilterSet):

    warranty_type = django_filters.CharFilter(name="warranty_type__label")

    class Meta:
        model = WarrantyContract

        fields =  [ 'warranty_type', 'contract_number', 'annual_cost', 'label', 'date_from', 'date_to' ]
