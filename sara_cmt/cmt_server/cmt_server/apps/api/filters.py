
import django_filters
from cmt_server.apps.cluster.models import HardwareUnit as Equipment

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

