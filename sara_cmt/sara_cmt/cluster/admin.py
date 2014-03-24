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
    list_filter  = ('cluster', 'rack', 'role', 'specifications', 'warranty') + \
        GlobalAdmin.list_filter
    inlines = [InterfaceInline]
    search_fields = ('label', 'warranty_tag')

    #change_list_template = "admin/change_list_filter_sidebar.html"


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
                           ('gateway', 'vlan'))}),
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
