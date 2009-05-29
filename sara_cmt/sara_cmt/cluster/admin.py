from django.contrib import admin
from sara_cmt.cluster.models import Cluster, Site, Contactperson, Rack, Interface, InterfaceType, HardwareUnit, Role, HardwareSpecifications, Network, Vendor, Warranty

# Some info about the Django admin site can be found at:
#   http://docs.djangoproject.com/en/dev/intro/tutorial02/#intro-tutorial02


class ClusterAdmin(admin.ModelAdmin):
  list_display = ('name',)
  fields       = ('name', 'note',)

class SiteAdmin(admin.ModelAdmin):
  list_display = ('name', 'address1', 'room', 'city', 'country',)
  list_filter  = ('city',)

class ContactpersonAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Summary', {
      'fields': ('firstname', 'lastname', ('site', 'vendor'),),
      'classes': ['wide'],
    }),
    ('Office', {
      'fields': ('address1', 'address2', 'room', 'postalcode', 'city', 'country'),
      'classes': ['wide'],
    }),
    ('Contact', {
      'fields': ('email', 'phone', 'fax',),
      'classes': ['wide'],
    }),
  )
  list_display  = ('__unicode__', 'email', 'phone',)
  list_filter   = ('site', 'vendor',)
  search_fields = ['lastname']

class RackAdmin(admin.ModelAdmin):
  fields       = ('site', 'label', 'capacity', 'note')
  list_display = ('site', 'label',)
  list_filter  = ('site',)
  ordering     = ('site',)

class InterfaceAdmin(admin.ModelAdmin):
  list_display = ('__unicode__', 'ip', 'hwaddress', 'type')
  list_filter  = ('network','type')

class InterfaceTypeAdmin(admin.ModelAdmin):
  list_display = ('label', 'vendor')
  list_filter  = ('vendor',)

class InterfaceInline(admin.TabularInline):
  model = Interface
  extra = 3

class HardwareUnitAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': (('cluster', 'role', 'specifications',),),
    }),
    ('Physical location', {
      'fields': (('rack', 'first_slot',),),
    }),
  )

  list_filter  = ('cluster', 'rack', 'role', 'specifications')
  list_display = ('__unicode__', 'cluster', 'rack', 'role', 'specifications')
  inlines = [InterfaceInline]

class RoleAdmin(admin.ModelAdmin):
  fields = ('label',)

class HardwareSpecificationsAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Vendor-specific', {
      'fields': ('vendor', 'name', 'system_id',),
    }),
    ('Dimensions', {
      'fields': ('slots_capacity', 'slots_size',),
    }),
  )

  list_display = ('vendor', 'name',)

class NetworkAdmin(admin.ModelAdmin):
  list_display = ('name', 'cidr', 'domain', 'prefix', '_max_hosts', 'count_ips_assigned', 'count_ips_free')
  fields       = ('name', 'netaddress', 'netmask', 'domain', 'prefix',)

class VendorAdmin(admin.ModelAdmin):
  fields       = ('name', 'address1', 'address2', 'postalcode', 'city', 'country',)
  list_display = ('name', 'address1', 'city', 'country',)

class WarrantyAdmin(admin.ModelAdmin):
  list_display = ('label', 'date_from', 'months', 'date_to',)




admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Contactperson, ContactpersonAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(InterfaceType, InterfaceTypeAdmin)
admin.site.register(HardwareUnit, HardwareUnitAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(HardwareSpecifications, HardwareSpecificationsAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Warranty, WarrantyAdmin)
