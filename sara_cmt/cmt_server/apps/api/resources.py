from djangorestframework.resources import ModelResource
from sara_cmt.cluster.models import Cluster, HardwareUnit, Network, WarrantyContract

class NetworkResource(ModelResource):
    model = Network
    fields = ('name', 'netaddress', 'netmask', 'gateway', 'domain', 'vlan')
    ordering = ('vlan',)

class EquipmentResource(ModelResource):
    model = HardwareUnit
    fields = ('cluster', 'role', 'network', 'specifications', 'warranty', 'rack', 'warranty_tag', 'first_slot', 'label',)
    ordering = ('rack', 'first_slot',)

class ClusterResource(ModelResource):
    model = Cluster
    fields = ('name',)

class ContractResource(ModelResource):
    model = WarrantyContract
    fields = ('label', 'date_from', 'date_to',)
    ordering = ('-date_to',)
