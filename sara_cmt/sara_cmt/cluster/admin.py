from django.contrib import admin
from sara_cmt.cluster.models import Cluster, Site, Contact, Rack, Interface, InterfaceType, HardwareUnit, Role, HardwareSpecifications, Network, Company, Department, Position, Warranty

# Some info about the Django admin site can be found at:
#   http://docs.djangoproject.com/en/dev/intro/tutorial02/#intro-tutorial02


class ClusterAdmin(admin.ModelAdmin):
  list_display = ('name',)
  fields       = ('name', 'note', 'tags')


class SiteAdmin(admin.ModelAdmin):
  list_display = ('name', 'address1', 'room', 'city', 'country')
  list_filter  = ('city',)


class ContactAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Summary', {
      'fields': ('firstname', 'lastname', 'employer', 'department', 'position', 'active', 'note'),
    }),
    ('Office', {
      'fields': ('address1', 'address2', 'room', 'postalcode', 'city', 'country'),
      'classes': ['wide'],
    }),
    ('Contact', {
      'fields': ('email', 'phone', 'cellphone', 'fax'),
      'classes': ['wide'],
    }),
  )
  list_display  = ('__unicode__', 'employer', 'department', 'position', 'email', 'phone', 'cellphone')
  list_filter   = ('employer', 'department', 'position', 'active')
  search_fields = ('firstname', 'lastname',)
  ordering      = ('lastname',)


class RackAdmin(admin.ModelAdmin):
  fields       = ('site', 'label', 'capacity', 'note', 'tags')
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
      #'fields': (('cluster', 'role', 'specifications', 'label'),),
    }),
    ('Physical location', {
      'fields': (('rack', 'first_slot',),),
    }),
  )

  list_display = ('__unicode__', 'cluster', 'rack', 'role', 'specifications')
  list_filter  = ('cluster', 'rack', 'role', 'specifications')
  inlines = [InterfaceInline]


class RoleAdmin(admin.ModelAdmin):
  fields = ('label', 'tags',)


class HardwareSpecificationsAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Vendor-specific', {
      'fields': ('vendor', 'name', 'system_id'),
    }),
    ('Dimensions', {
      'fields': ('slots_capacity', 'slots_size',),
    }),
  )

  list_display = ('vendor', 'name',)


class NetworkAdmin(admin.ModelAdmin):
  list_display = ('name', 'cidr', 'domain', 'prefix', '_max_hosts', 'count_ips_assigned', 'count_ips_free')
  fields       = ('name', 'netaddress', 'netmask', 'domain', 'prefix', 'tags')


class CompanyAdmin(admin.ModelAdmin):
  fields       = ('name', 'vendor', 'address1', 'address2', 'postalcode', 'city', 'country', 'website', 'tags')
  list_display = ('name', 'address1', 'city', 'country', 'website')
  list_filter  = ('country',)


class PositionAdmin(admin.ModelAdmin):
  fields = ('label', 'tags',)


class DepartmentAdmin(admin.ModelAdmin):
  fields = ('label', 'tags',)


class WarrantyAdmin(admin.ModelAdmin):
  list_display = ('label', 'date_from', 'months', 'date_to')




admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(InterfaceType, InterfaceTypeAdmin)
admin.site.register(HardwareUnit, HardwareUnitAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(HardwareSpecifications, HardwareSpecificationsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Warranty, WarrantyAdmin)
