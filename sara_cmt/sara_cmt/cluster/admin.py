#    This file is part of CMT, a Cluster Management Tool made at SURFsara.
#    Copyright (C) 2012, 2013  Sil Westerveld, Ramon Bastiaans
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from django.contrib import admin

from sara_cmt.cluster.models import Cluster, HardwareUnit, Interface, Network, Rack
from sara_cmt.cluster.models import Country, Address, Room
from sara_cmt.cluster.models import Company, Telephonenumber, Connection
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyContract, WarrantyType

from django.contrib.admin import SimpleListFilter

# Some info about the Django admin site can be found at:
#   http://docs.djangoproject.com/en/dev/intro/tutorial02/#intro-tutorial02



######
#
# A global admin to inherit from
#


class GlobalAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    fields = ('note',)
    list_filter = ('created_on', 'updated_on' )
    list_per_page = 50
    extra_fieldset = ('Additional fields', {
        'fields': fields,
        'classes': ('collapse',)})


class CMTAdmin(admin.ModelAdmin):

    change_list_template = 'smuggler/change_list.html'

    save_as = True

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
    exclude = GlobalAdmin.fields + ('tags',)

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


class ClusterAdmin(CMTAdmin):
    fields       = ('name','machinenames') + GlobalAdmin.fields
    list_display = ('name','machinenames')
    list_filter  = GlobalAdmin.list_filter


class ClusterListFilter(SimpleListFilter):
 
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Cluster'
 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'cluster'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        clusters = set([c.cluster for c in model_admin.model.objects.all()])

        lookups = [ ]

        for c in clusters:

            c_count_str = ' (%d)' %len( model_admin.model.objects.filter( cluster__name=c.name ) )

            lookups.append( (c.id, c.name + c_count_str ) )

        return lookups
 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(cluster__id=self.value())
        else:
            return queryset

class HardwareUnitAdmin(CMTAdmin):
    fieldsets = (
        ('Host info', {'fields': (('cluster', 'label'),)}),
        ('Configuration', {'fields': (('state', 'role'),)}),
        ('Machine specifications', {'fields': ('specifications', 'warranty',
                                               'warranty_tag', 'serial_number')}
        ),
        ('Physical location', {'fields': (('rack', 'first_slot'),)}),
        ('Involved parties', {'fields': ('seller', 'owner')}),
        GlobalAdmin.extra_fieldset)

    list_display = ('__unicode__', 'warranty_tag', 'cluster', 'address', 'room', 'rack',
        'first_slot', 'specifications', 'roles', 'in_support')
    list_filter  = (ClusterListFilter, 'rack', 'role', 'specifications', 'warranty') + \
        GlobalAdmin.list_filter
    inlines = [InterfaceInline]
    search_fields = ('label', 'warranty_tag')



class CountryAdmin(CMTAdmin):
    fieldsets = (
        ('None', {'fields': (('name', 'country_code'),)}),
        GlobalAdmin.extra_fieldset)
    list_display = ('country_code', 'name')
    list_filter  = GlobalAdmin.list_filter


class AddressAdmin(CMTAdmin):
    fieldsets = (
        ('Location', {'fields': ('address', 'postalcode', 'city', 'country'),
                      'classes': ('wide',)}),
        GlobalAdmin.extra_fieldset)
    list_display  = ('address', 'postalcode', 'city', 'country', 'companies')
    list_filter   = ('country', 'city') + GlobalAdmin.list_filter
    search_fields = ('address',)

    inlines = [RoomInline]


class RoomAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': (('address', 'floor', 'label'),)}),
        GlobalAdmin.extra_fieldset)
    list_filter = ('address', 'floor') + GlobalAdmin.list_filter
    list_display = ('address', 'floor', 'label')


class ConnectionAdmin(CMTAdmin):
    fieldsets = (
        ('Summary', {
            'fields': (('name', 'active'), ('email', 'company', 'address')),
            'classes': ['wide']
        }),
        GlobalAdmin.extra_fieldset)
    list_display  = ('__unicode__', 'company', 'email')
    list_filter   = ('company', 'active') + GlobalAdmin.list_filter
    search_fields = ('name',)
    inlines       = [PhoneInline]


class RackAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': (('room', 'label', 'capacity'),)}),
        GlobalAdmin.extra_fieldset)
    list_display = ('label', 'address', 'room')
    list_filter  = ('room',) + GlobalAdmin.list_filter


class InterfaceAdmin(CMTAdmin):
    fieldsets = (
        ('Physical', {'fields': (('iftype', 'host'), ('hwaddress', 'ip'))}),
        ('Network', {'fields': ('network', ('label', 'aliases'))}),
        GlobalAdmin.extra_fieldset)
    list_display = ('__unicode__', 'network', 'hwaddress', 'ip', 'iftype')
    list_filter  = ('network', 'iftype') + GlobalAdmin.list_filter
    search_fields = ('label', 'aliases', 'hwaddress', 'ip', 'host__label')


class InterfaceTypeAdmin(CMTAdmin):
    fieldsets = (
        ('Properties', {'fields': (('label', 'vendor'),)}),
        GlobalAdmin.extra_fieldset)
    list_display = ('label', 'vendor')
    list_filter  = ('vendor',) + GlobalAdmin.list_filter


class RoleAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': ('label',)}),
        GlobalAdmin.extra_fieldset)
    list_filter = GlobalAdmin.list_filter


class HardwareModelAdmin(CMTAdmin):
    fieldsets = (
        ('Vendor-specific', {'fields': ('vendor', 'name', 'vendorcode')}),
        ('Dimensions', {'fields': (('rackspace', 'expansions'),)}),
        GlobalAdmin.extra_fieldset)

    list_display = ('vendor', 'name' )
    list_filter  = ('vendor', ) + GlobalAdmin.list_filter


class NetworkAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': (('name', 'hostnames', 'domain'),
                           ('cidr', 'gateway', 'vlan'))}),
        GlobalAdmin.extra_fieldset)
    list_display = ('name', 'vlan', 'cidr', 'gateway', 'domain', 'hostnames',
                    'count_ips_assigned', 'count_ips_free')
    list_filter  = GlobalAdmin.list_filter


class CompanyAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': ('name', )}),
        ('Contact info', {'fields': ('website', 'addresses')}),
        GlobalAdmin.extra_fieldset)
    list_display = ('name', 'website', 'get_addresses')
    list_filter  = GlobalAdmin.list_filter
    filter_horizontal = ('addresses', )


class TelephonenumberAdmin(CMTAdmin):
    fieldsets = (
        ('Owner', {'fields': (('connection', 'number_type'),)}),
        ('Number', {'fields': (('country', 'areacode', 'subscriber_number'),)}),
        GlobalAdmin.extra_fieldset)
    list_display = ('connection', 'number_type', '__unicode__')
    list_filter  = ('number_type', 'country', 'areacode') + GlobalAdmin.list_filter


class WarrantyContractAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': (('label', 'warranty_type'), ('contract_number', 'annual_cost'))}),
        ('Period', {'fields': (('date_from', 'date_to'),)}),
        GlobalAdmin.extra_fieldset)

    list_display = ('label', 'date_from', 'date_to', 'expired')
    list_filter  = ('date_to', ) + GlobalAdmin.list_filter


class WarrantyTypeAdmin(CMTAdmin):
    fieldsets = (
        (None, {'fields': (('label', 'contact'),)}),
        GlobalAdmin.extra_fieldset)

    list_display = ('label', 'contact')
    list_filter  = GlobalAdmin.list_filter


admin.site.register(Cluster, ClusterAdmin)
admin.site.register(HardwareUnit, HardwareUnitAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Rack, RackAdmin)

admin.site.register(Country, CountryAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Room, RoomAdmin)

admin.site.register(Company, CompanyAdmin)
admin.site.register(Telephonenumber, TelephonenumberAdmin)
admin.site.register(Connection, ConnectionAdmin)

admin.site.register(HardwareModel, HardwareModelAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(InterfaceType, InterfaceTypeAdmin)

admin.site.register(WarrantyContract, WarrantyContractAdmin)
admin.site.register(WarrantyType, WarrantyTypeAdmin)
