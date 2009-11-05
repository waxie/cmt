from django.contrib import admin

from sara_cmt.cluster.models import Cluster, HardwareUnit, Alias, Interface, Network, Rack
from sara_cmt.cluster.models import Country, Address, Room, Site
from sara_cmt.cluster.models import Company, Telephonenumber, Connection
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyContract, WarrantyType

# Some info about the Django admin site can be found at:
#   http://docs.djangoproject.com/en/dev/intro/tutorial02/#intro-tutorial02



######
#
# A global admin to inherit from
#

class GlobalAdmin(admin.ModelAdmin):
  date_hierarchy = 'created_on'
  fields = ('note', 'tags')
  list_filter = ('created_on', 'updated_on', 'tags')
  list_per_page = 50
  extra_fieldset = ('Additional fields', {'fields': fields, 'classes': ('collapse',)})

#
#
#
######



######
#
# Inlines
#

class AddressInline(admin.TabularInline):
  model = Address
  exclude = GlobalAdmin.fields
  

class InterfaceInline(admin.TabularInline):
  model = Interface
  exclude = GlobalAdmin.fields
  extra = 3


class PhoneInline(admin.TabularInline):
  model = Telephonenumber
  exclude = GlobalAdmin.fields


class RoomInline(admin.TabularInline):
  model = Room
  exclude = GlobalAdmin.fields

#
#
#
######



class ClusterAdmin(admin.ModelAdmin):
  fields       = ('name',) + GlobalAdmin.fields
  list_display = ('name',) + GlobalAdmin.list_display
  list_filter  = GlobalAdmin.list_filter


class HardwareUnitAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Host info', {
      'fields': (('cluster', 'label', 'role'),),
    }),
    ('Machine specifications', {
      'fields': (('specifications', 'warranty'),('service_tag', 'serialnumber'))
    }),
    ('Physical location', {
      'fields': (('rack', 'first_slot'),)
    }),
    GlobalAdmin.extra_fieldset
  )

  list_display = ('__unicode__', 'cluster', 'address', 'room', 'rack', 'first_slot', 'specifications', 'roles', 'in_support')
  list_filter  = ('cluster', 'rack', 'role', 'specifications') + GlobalAdmin.list_filter
  inlines = [InterfaceInline]

  #filter_horizontal = ('role',)


class SiteAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {'fields': ('name',)}),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('name',) + GlobalAdmin.list_filter
  list_filter  = GlobalAdmin.list_filter
  ordering     = ('name',)


class CountryAdmin(admin.ModelAdmin):
  fieldsets = (
    ('None', {'fields': (('name', 'country_code'),)}),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('country_code', 'name')
  list_filter  = GlobalAdmin.list_filter
  ordering = ('name',)


class AddressAdmin(admin.ModelAdmin):
  #date_hierarchy = 'created_on'
  fieldsets = (
    ('Location', {'fields': ('address', 'postalcode', 'city', 'country'), 'classes': ('wide',)}),
    GlobalAdmin.extra_fieldset
  )
  list_display  = ('address', 'postalcode', 'city', 'country', 'companies')
  list_filter   = ('city', 'country') + GlobalAdmin.list_filter
  search_fields = ('address',)
  
  inlines = [RoomInline]


class RoomAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {'fields': (('address', 'floor', 'label'),)}),
    GlobalAdmin.extra_fieldset
  )
  list_filter = ('address', 'floor') + GlobalAdmin.list_filter
  list_display = ('address', 'floor', 'label')
  ordering = ('address', 'floor')


class ConnectionAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Summary', {
      'fields': (('name', 'active'), ('email', 'company', 'address')),
      'classes': ['wide'],
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display  = ('__unicode__', 'company', 'email')
  list_filter   = ('company', 'active') + GlobalAdmin.list_filter
  search_fields = ('name',)
  #ordering      = ('name',)
  inlines       = [PhoneInline]


class RackAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': (('room', 'label', 'capacity'),),
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('address', 'room', 'label',)
  list_filter  = ('room',) + GlobalAdmin.list_filter
  ordering     = ('room',)


class AliasAdmin(admin.ModelAdmin):
  pass


class InterfaceAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Physical', {
      'fields': (('type', 'hardware'), 'hwaddress'),
    }),
    ('Network', {
      'fields': ('network', ('label', 'aliasses')),
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('__unicode__', 'hwaddress', 'type')
  list_display = ('__unicode__', 'ip', 'hwaddress', 'type')
  list_filter  = ('network','type',) + GlobalAdmin.list_filter


class InterfaceTypeAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Properties', {
      'fields': ('label', 'vendor'),
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('label', 'vendor')
  list_filter  = ('vendor',) + GlobalAdmin.list_filter


class RoleAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {'fields': ('label',)}),
    GlobalAdmin.extra_fieldset
  )
  list_filter = GlobalAdmin.list_filter


class HardwareModelAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Vendor-specific', {
      'fields': ('vendor', 'name'),
      #'fields': ('vendor', ('name', 'model_id')),
    }),
    ('Dimensions', {
      'fields': ('expansions', 'rackspace'),
    }),
    GlobalAdmin.extra_fieldset
  )

  list_display = ('vendor', 'name', 'tags')
  list_filter  = ('vendor', 'tags') + GlobalAdmin.list_filter


class NetworkAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': (('name', 'hostnames', 'domain'), ('netaddress', 'netmask', 'vlan')),
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('name', 'vlan', 'cidr', 'domain', 'hostnames', '_max_hosts', 'count_ips_assigned', 'count_ips_free')
  list_filter  = GlobalAdmin.list_filter


class CompanyAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('name',),
    }),
    ('Contact info', {
      'fields': ('website', 'addresses'),
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('name', 'website', 'get_addresses')
  list_filter  = GlobalAdmin.list_filter
  filter_horizontal = ('addresses',)


class TelephonenumberAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Owner', {
      'fields': (('connection', 'type'),)
    }),
    ('Number', {
      'fields': (('country', 'areacode', 'subscriber_number'),)
    }),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('connection', 'type', '__unicode__')
  list_filter  = ('type', 'country', 'areacode') + GlobalAdmin.list_filter


class WarrantyContractAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('label', 'type'),
    }),
    ('Period', {
      'fields': ('date_from', 'date_to'),
    }),
    GlobalAdmin.extra_fieldset
  )

  list_display = ('label', 'date_from', 'date_to', 'expired')
  list_filter  = GlobalAdmin.list_filter


class WarrantyTypeAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('label', 'contact'),
    }),
    GlobalAdmin.extra_fieldset
  )
  
  list_display = ('label', 'contact')
  list_filter  = GlobalAdmin.list_filter




admin.site.register(Cluster, ClusterAdmin)
admin.site.register(HardwareUnit, HardwareUnitAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Rack, RackAdmin)

admin.site.register(Country, CountryAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Site, SiteAdmin)

admin.site.register(Company, CompanyAdmin)
admin.site.register(Telephonenumber, TelephonenumberAdmin)
admin.site.register(Connection, ConnectionAdmin)

admin.site.register(HardwareModel, HardwareModelAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(InterfaceType, InterfaceTypeAdmin)

admin.site.register(WarrantyContract, WarrantyContractAdmin)
admin.site.register(WarrantyType, WarrantyTypeAdmin)
