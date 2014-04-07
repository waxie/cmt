
import django_filters
from cmt_server.apps.cluster.models import HardwareUnit as Equipment

class EquipmentFilter(django_filters.FilterSet):

    cluster = django_filters.CharFilter(name="cluster__name")
    rack = django_filters.CharFilter(name="rack__label")

    class Meta:
        model = Equipment

        fields =  [
            'cluster', 'rack',
            'serial_number', 'first_slot', 'label'
            ]

        order_by = 'label'

