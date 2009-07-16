from django.contrib import admin

from sara_cmt.cluster.models import Cluster, HardwareUnit, Interface, Network, Rack
from sara_cmt.cluster.models import Address, Room, Site
from sara_cmt.cluster.models import Company, Telephonenumber, Connection
from sara_cmt.cluster.models import HardwareSpecifications, Role, InterfaceType
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
  extra_fieldset = ('Additional', {'fields': fields, 'classes': ('collapse',)})

#
#
#
######



######
#
# Inlines
#

class InterfaceInline(admin.TabularInline):
  model = Interface
  exclude = GlobalAdmin.fields
  extra = 3


class PhoneInline(admin.TabularInline):
  model = Telephonenumber
  #model = Connection
  exclude = GlobalAdmin.fields
  #fk_name = 'phone'


class CellphoneInline(admin.TabularInline):
  model = Telephonenumber
  #model = Connection
  exclude = GlobalAdmin.fields
  #fk_name = 'cellphone'


class FaxInline(admin.TabularInline):
  model = Telephonenumber
  #model = Connection
  exclude = GlobalAdmin.fields
  #fk_name = 'fax'

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
    (None, {
      'fields': (('cluster', 'specifications', 'warranty', ),),
      #'fields': (('cluster', 'role', 'specifications', 'warranty', ),),
      #'fields': (('cluster', 'role', 'specifications', 'label'),),
    }),
    ('Physical location', {
      'fields': (('rack', 'first_slot',),),
    }),
  )

  list_display = ('__unicode__', 'cluster', 'rack', 'specifications')
  #list_display = ('__unicode__', 'cluster', 'rack', 'role', 'specifications')
  list_filter  = ('cluster', 'rack', 'specifications')
  #list_filter  = ('cluster', 'rack', 'role', 'specifications')
  inlines = [InterfaceInline]


class SiteAdmin(admin.ModelAdmin):
  fields       = ('name',) + GlobalAdmin.fields
  list_display = ('name',) + GlobalAdmin.list_filter
  list_filter  = GlobalAdmin.list_filter
  ordering     = ('name',)


class AddressAdmin(admin.ModelAdmin):
  #date_hierarchy = 'created_on'
  fieldsets = (
    ('Location', {'fields': (('address1', 'address2'), ('postalcode', 'city'), 'country'), 'classes': ('wide',)}),
    GlobalAdmin.extra_fieldset
  )
  list_display = ('address1', 'postalcode', 'city', 'country')
  list_filter  = ('city', 'country') + GlobalAdmin.list_filter
  search_fields = ('address1',)


class RoomAdmin(admin.ModelAdmin):
  list_filter = ('address', 'floor')


class ConnectionAdmin(admin.ModelAdmin):
  #fieldsets = (
  #  ('Summary', {
  #    'fields': ('firstname', 'lastname', 'employer', 'active', 'note'),
  #  }),
  #  ('Office', {
  #    'fields': ('address1', 'address2', 'postalcode', 'city', 'country'),
  #    'classes': ['wide'],
  #  }),
  #  ('Contact', {
  #    'fields': ('email', 'phone', 'cellphone', 'fax'),
  #    'classes': ['wide'],
  #  }),
  #)
  list_display  = ('__unicode__', 'employer', 'email')#, 'phone', 'cellphone')
  list_filter   = ('employer', 'active')
  search_fields = ('firstname', 'lastname',)
  ordering      = ('lastname',)
  inlines = [PhoneInline]#, CellphoneInline, FaxInline]


class RackAdmin(admin.ModelAdmin):
  fields       = ('address', 'label', 'capacity', 'note',)
  list_display = ('address', 'label',)
  list_filter  = ('address',)
  ordering     = ('address',)


class InterfaceAdmin(admin.ModelAdmin):
  list_display = ('__unicode__', 'ip', 'hwaddress', 'type')
  list_filter  = ('network','type',)


class InterfaceTypeAdmin(admin.ModelAdmin):
  list_display = ('label', 'vendor',)
  list_filter  = ('vendor',)


class RoleAdmin(admin.ModelAdmin):
  fields = ('label',)


class HardwareSpecificationsAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Vendor-specific', {
      'fields': ('vendor', 'name', 'system_id'),
    }),
    ('Dimensions', {
      'fields': ('slots_capacity', 'slots_size'),
    }),
  )

  list_display = ('vendor', 'name')


class NetworkAdmin(admin.ModelAdmin):
  list_display = ('name', 'cidr', 'domain', 'prefix', '_max_hosts', 'count_ips_assigned', 'count_ips_free')
  fields       = ('name', 'netaddress', 'netmask', 'domain', 'prefix',)


class CompanyAdmin(admin.ModelAdmin):
  fields       = ('name', 'website', 'buildings')
  list_display = ('name', 'website')
  filter_horizontal = ('buildings',)


#class TelephonenumberAdmin(admin.ModelAdmin):
#  pass
#  #list_filter = ('country_code', 'areacode')


class WarrantyContractAdmin(admin.ModelAdmin):
  list_display = ('label', 'date_from', 'months', 'date_to')


class WarrantyTypeAdmin(admin.ModelAdmin):
  list_display = ('label', 'contact')




#admin.site.register(Cluster, ClusterAdmin)
admin.site.register(HardwareUnit, HardwareUnitAdmin)
#admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Rack, RackAdmin)

admin.site.register(Address, AddressAdmin)
admin.site.register(Room, RoomAdmin) #
admin.site.register(Site, SiteAdmin)

#admin.site.register(Company, CompanyAdmin)
#admin.site.register(Telephonenumber, TelephonenumberAdmin) #
#admin.site.register(Telephonenumber) #
admin.site.register(Connection, ConnectionAdmin)

#admin.site.register(HardwareSpecifications, HardwareSpecificationsAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(InterfaceType, InterfaceTypeAdmin)

admin.site.register(WarrantyContract, WarrantyContractAdmin)
admin.site.register(WarrantyType, WarrantyTypeAdmin) #
