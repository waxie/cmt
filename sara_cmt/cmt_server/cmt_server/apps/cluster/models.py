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

from django.db import models
from django.core.validators import RegexValidator

from django.core.exceptions import ValidationError

import re
from datetime import date

from psycopg2 import IntegrityError

from IPy import IP

from cmt_server.logger import Logger
logger = Logger().getLogger()

#from django_extensions.db.fields import CreationDateTimeField, \
#                                        ModificationDateTimeField

class CMTModel(models.Model):
    """
        The CMTModel is meant as a Mixin with some fields that have to
        exist in every model used in CMT.
    """
# Use of CreationDateTimeField and ModificationDateTimeField might not be needed
# anymore, since Django now has DateField.auto_now_add and DateField.auto_now
#    created_on = CreationDateTimeField()
#    updated_on = ModificationDateTimeField()
    created_on = DateField(auto_now_add=True)
    updated_on = DateField(auto_now=True)
    note = models.TextField(blank=True, help_text='Any additional information to store.')

    class Meta:
        abstract = True


#####
#
# <STATIC METHODS>
#

    @staticmethod
    def display(instance):
        """
            Print all values given in list_display of the model's admin
        """
        # First get access to the admin
        admin_class_name = instance._meta.object_name + 'Admin'
        import cmt_server.apps.cluster.admin
        admin_list_display = eval('cmt_server.apps.cluster.admin.' \
                                + admin_class_name + '.list_display')

        # Determine longest value-string to display
        longest_key = 0
        for val in admin_list_display:
            if len(val) > longest_key:
                longest_key = len(val)

        # Print the values
        print ' .---[  %s  ]---' % instance
        for key in admin_list_display:
            if key not in ('__unicode__', '__str__'):
                print ' : %s : %s' % (key.ljust(longest_key), \
                                      instance.__getattribute__(key))
        print " '---\n"
#
# </STATIC METHODS>
#
#####

class Cluster(CMTModel):
    """
        A labeled group of hardware pieces.
    """
    # Fields:
    label        = models.CharField(max_length=255, unique=True)

    equipment_labeling = models.CharField(max_length=255, blank=True, null=True,
                           help_text='Used as a template for physical labeling of Equipment')
    host_labeling = models.CharField(max_length=255, blank=True, null=True,
                      help_text='Used as a template for labels of Host-instances in the cluster. <TODO: example>')

    class Meta:
        ordering = ('label',)

    def __unicode__(self):
        return unicode(self.label) or None


class Equipment(CMTModel):
    """
        A specific piece of hardware.
    """
    # Relations:
    cluster  = models.ForeignKey('Cluster', related_name='equipment')
    equipment_type = models.ForeignKey('EquipmentType', related_name='equipment', blank=True, null=True)
    network  = models.ManyToManyField('Network', related_name='equipment', through='Interface')
    rack     = models.ForeignKey('Rack', related_name='contents')
    role     = models.ManyToManyField('Role', related_name='equipment')
    warranty = models.ForeignKey('Warranty', related_name='equipment', blank=True, null=True)

    # Fields:
    label         = models.CharField(max_length=255)

    node          = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True, unique=True)
    warranty_code = models.CharField(max_length=255, blank=True, null=True, unique=True,
                                     help_text='Service tag')

    class Meta:
        verbose_name_plural = "equipment"
        ordering = ('rack__label', 'node')
        unique_together = (('rack', 'node'), ('cluster', 'label'))

    @property
    def address(self):
        return self.rack.address

    @property
    def in_support(self):
        retval = False
        try:
            assert bool(self.warranty), 'No warranty contract for %s %s' % \
                (self.__class__.__name__, self.label)
            retval = not self.warranty.expired
        except:
            retval = False
            logger.warning("Hardware with label '%s' hasn't got a warranty \
                contract" % self.label)
        return retval

    @property
    def roles(self):
        return [str(role.label) for role in self.role.all()]

    @property
    def room(self):
        return self.rack.room

    def __unicode__(self):
        try:
            assert self.label, "piece of hardware hasn't got a label yet"
            return unicode(self.label)
        except AssertionError, e:
            return unicode(e)

    def save(self, force_insert=False, force_update=False):
        """
            First check if the label has already been filled in. If it's still
            empty, then set it to the default basename (based on rack# and
            node#).
        """
        if not self.label:
            self.label = self.default_label()

        # Solution for empty unique fields described on:
        # http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
        if not self.node:
            self.node = None
        if not self.serial_number:
            self.serial_number = None
        if not self.warranty_code:
            self.warranty_code = None

        super(Equipment, self).save(force_insert, force_update)

    def default_label(self):
        try:
            assert self.rack.label is not None and self.node is not \
                None, 'not able to generate a label'

            if self.cluster.machinenames is not None and self.cluster.machinenames != '':
                machine_label = self.cluster.machinenames.format( rack=self.rack.label, node=self.first_slot )
            else:
                #RB: fail back to previous default behaviour
                machine_label = 'r%sn%s' %(self.rack.label, self.node)

            assert machine_label.find( '{' ) == -1, \
                'unable to format cluster machine name: %s' %machine_label

            return machine_label
        except:
            pass


class EquipmentType(CMTModel):
    """
        This model is being used to specify some extra information about a
        specific type (model) of hardware.
    """
    # Relations:
    contact = models.ForeignKey('ContactInfo', related_name='model specifications')

    # Fields:
    label       = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'model'
        ordering = ('contact', 'name')

    def __unicode__(self):
        return unicode('%s (%s)' % (self.label, self.contact))


class Role(CMTModel):
    """
        This describes a possible role of a Equipment in the cluster. A piece of
        hardware can have a role like 'switch', 'compute node', 'patchpanel', 'pdu',
        'admin node', 'login node', etc...
        Those roles can be used for all kinds of rules on Equipments which exist
        in the cluster.
    """
    # Fields:
    label = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('label',)
        verbose_name = 'role'
        verbose_name_plural = 'roles'

    def __unicode__(self):
        return unicode(self.label)


class Warranty(CMTModel):
    """
        A class which contains warranty information of (a collection of) hardware. (SLA)
    """
    # Relations:
    contacts = ManyToManyField('ContactInfo', related_name='people and/or departments involved'
    warranty_type = models.ForeignKey('WarrantyType', blank=True, null=True, related_name='contracts')

    # Fields:
    label     = models.CharField(max_length=255, unique=True)

    contract_number = models.CharField(max_length=255, blank=True, null=True, unique=True,
                        help_text='NSEN420201')
    date_from = models.DateField(verbose_name='valid from')
    date_to   = models.DateField(verbose_name='expires at')
    date_to.in_support_filter = True

    class Meta:
        ordering = ('label',)

    @property
    def expired(self):
        return self.date_to < date.today()

    def __unicode__(self):
        return unicode(self.label)

    def save(self, force_insert=False, force_update=False):
        """
            The contract number is an optional field, but when filled in it
            should have a unique value. When kept blank, it should be stored as
            None.
        """
        if not self.contract_number:
            self.contract_number = None

        super(Warranty, self).save(force_insert, force_update)


class WarrantyType(CMTModel):
    """
        A type of warranty offered by a company.
    """
    # Relations:
    contact = models.ForeignKey('Connection', related_name='warranty types')

    # Fields:
    label = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('contact__company__name', 'label')
    def __unicode__(self):
        return unicode(self.label)


class Rack(CMTModel):
    """
        A Rack is a standardized system for mounting various Equipments in a
        stack of slots.
    """
    # Relations:
    room = models.ForeignKey('Room', related_name='racks')

    # Fields:
    label    = models.CharField(max_length=255)

    class Meta:
        unique_together = ('room', 'label')
        ordering = ('label',)
        verbose_name = 'rack'
        verbose_name_plural = 'racks'

    @property
    def address(self):
        return self.room.address

    def __unicode__(self):
        return unicode('rack %s' % (self.label) )


class Room(CMTModel):
    """
        A room is located at an address. This is where racks of hardware can be
        found.
    """
    # Relations:
    address = models.ForeignKey('Address', related_name='rooms')

    # Fields:
    label   = models.CharField(max_length=255, blank=False)

    floor   = models.IntegerField(max_length=2)

    class Meta:
        unique_together = ('address', 'floor', 'label')
        ordering = ('address__postalcode', 'floor')

    def __unicode__(self):
        #return unicode('%s - %s'%(self.address,self.label))
        return unicode('%s (%s, %s)' % (self.label, self.address.address, self.address.city))


class Address(CMTModel):
    """
        A class to hold information about the physical location of a model.
    """
    # Fields:
    address    = models.CharField(max_length=255)
    city       = models.CharField(max_length=255)
    country    = models.CharField(max_length=255)
    postalcode = models.CharField(max_length=9, blank=True)

    @property
    def contacts(self):
        return ' | '.join([c.label for c in self._contacts.all()]) or '-'

    class Meta:
        unique_together = ('address', 'city')
        verbose_name_plural = 'addresses'
        ordering = ('postalcode',)

    def __unicode__(self):
        return unicode('%s - %s' % (self.city, self.address))


class ContactInfo(CMTModel):
    """
        The ContactInfo-model can be linked to Equipment. This way you are able to define
        contactpersons for a specific piece of hardware.
    """
    # Relations:
    addresses = models.ForeignKey('Address', related_name='_contacts')

    # Fields:
    label   = models.CharField(max_length=255)

    company = models.CharField(max_length=255)
    email  = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=255)
    website = models.URLField()

    def get_addresses(self):
        return ' | '.join([a.address for a in self.addresses.all()]) or '-'

    def __unicode__(self):
        return unicode(self.label)

    class Meta:
        ordering = ('label',) 


class Interface(CMTModel):
    """
        An interface of a piece of hardware.
    """
    # Validators
    re_valid_mac      = re.compile(r'([A-Fa-f\d]{2}[:-]?){5}[A-Fa-f\d]{2}')
    re_mac_octets     = re.compile(r'[A-Fa-f\d]{2}')
    re_valid_cnames   = re.compile(r'^[a-z\d\-\.]+([,]{1}[a-z\d\-\.]+)*$')

    # valid hostname  = 1-63 length, lowercase, numbers and hyphen (-). May not begin/end with hyphen
    re_valid_hostname = re.compile(r'^([0-9a-z]{1,2})$|^([a-z0-9]{1})([a-z0-9\-]{1,61})([a-z0-9]{1})$')

    hwaddress_validator = RegexValidator(re_valid_mac,'Enter a valid MAC address. Example: "cc:cc:cc:cc:cc:cc". Valid characters: [a-f], [A-F], [0-9] and ":"', 'invalid')
    cnames_validator    = RegexValidator(re_valid_cnames,'One or more (comma seperated, no spaces) aliases. Example: "test,test.console,alias2". Valid characters: [a-z], [0-9], "-", "." and ","', 'invalid')
    hostname_validator  = RegexValidator(re_valid_hostname,'Enter a valid hostname. Example: "myhostname-rack2node3". Valid characters: [a-z], [0-9] and "-"','invalid')

    # Relations:
    equipment      = models.ForeignKey('Equipment', related_name='interfaces', verbose_name='equipment')
    interface_type = models.ForeignKey('InterfaceType', related_name='interfaces', verbose_name='type')
    network        = models.ForeignKey('Network', related_name='interfaces')
    # Fields:
    label     = models.CharField(max_length=255, help_text='Automagically \
                                 generated if kept empty', validators=[hostname_validator])

    hwaddress = models.CharField(max_length=17, blank=True, null=True,
                                 verbose_name='hardware address',
                                 help_text="6 Octets, optionally delimited by \
                                 a space ' ', a hyphen '-', or a colon ':'.",
                                 validators=[hwaddress_validator])
    ip        = models.GenericIPAddressField(blank=True, protocol='both')

    class Meta:
        unique_together = ('network', 'hwaddress')
        ordering = ('host__cluster__name', 'host__rack__label', 'host__node')

    # TODO: Implement properties for primary_host and secondary_hosts

    def __unicode__(self):
        #return self.fqdn
        return unicode(self.label) or unicode('anonymous')

    def clean(self):

        """
        Non field errors are validated here
        """

        network = IP('%s' % (self.network.cidr) )

        # If IP is given, make sure it is in the subnet
        if self.ip is not None and self.ip != '':
            ip = IP(self.ip)

            if ip not in network:
                raise ValidationError('IP addresses %s is not in subnet: %s (%s)' %(self.ip, self.network.cidr, self.network.name ) )

        # Pick a new IP when it's not defined yet or when the network has
        # been changed
        if self.ip is None or self.ip == '':
            self.ip = self.network.pick_ip()

        if self.ip is None or self.ip == '':
            raise ValidationError('No more IP addresses available in: %s' %self.network.name )

    def save(self, force_insert=False, force_update=False):
        """
            First check for a correct IP address before saving the object.
            Pick a new one in the related network when the IP hasn't been set
            yet, or when the network has been changed.
        """
        try:
            if not self.hwaddress:
                self.hwaddress = None

            if self.hwaddress and len(self.hwaddress) >= 12:
                self.hwaddress = ':'.join(self.re_mac_octets.findall(self.hwaddress.lower()))
            # To be sure that the interface has a valid network
            #assert isinstance(self.network, Network), "network doesn't exist"

            try:
                if self.network:
                    network = IP('%s' % (self.network.cidr) )

            except ValueError, e:
                print ValueError, e
            except Exception, e:
                print 'An error occured:', e

            self.label = self.label or \
                         self.network.construct_interface_label(self.host)

            try:
                super(Interface, self).save(force_insert, force_update)
            except IntegrityError, e:
                logger.error(e)
        except AssertionError, e: # !!! TODO: exception on other errors !!!
            print AssertionError, e


class InterfaceType(CMTModel):
    """
        Contains information about different types of interfaces.
    """
    # Fields:
    label = models.CharField(max_length=255, help_text="'DRAC 4' for example")

    class Meta:
        # Note in docs of Model Meta options,
        # see http://docs.djangoproject.com/en/dev/ref/models/options/#ordering
        # "Regardless of how many fields are in ordering, the admin site uses
        # only the first field."
        #ordering = ('vendor', 'label')
        ordering = ('label',)
        verbose_name = 'type of interface'
        verbose_name_plural = 'types of interfaces'

    def __unicode__(self):
        return self.label


class Network(CMTModel):
    """
        Class with information about a network. Networks are connected with
        Interfaces (and Equipments as equipment through Interface).
    """

    # Fields:
    label      = models.CharField(max_length=255, help_text='example: infiniband')

    cidr       = models.CharField(max_length=100, help_text='example: 192.168.1.0/24 or fd47:e249:06b2:0385::/64')
    gateway    = models.GenericIPAddressField(blank=True, help_text='Automagically generated if kept empty')
    interface_labeling = models.CharField(max_length=255, blank=True, null=True, help_text='how interfaces in this network should be labeled in the OS')
    reserved_ips = models.CharField(max_length=255, blank=True, null=True, help_text='notation based on CIDR-notation, with boolean expressions like "!", "|", "(" and ")" and "/32" for a single IP')
    vlan       = models.PositiveIntegerField(max_length=3, null=True,
                                             blank=True)

    class Meta:
        ordering = ('name')
        verbose_name = 'network'
        verbose_name_plural = 'networks'

    def __unicode__(self):
        return unicode(self.name)

    #
    def _rev_name(self):
        network = IP("%s" % (self.cidr))
        reverse_name = network.reverseName()
        return reverse_name

    #
    def _rev_names(self):
        network = IP("%s" % (self.cidr))
        reverse_names = network.reverseNames()
        return reverse_names

    def _max_hosts(self):
        """
            Give the total amount of IP-addresses which could be assigned to hosts in
            this network.

            Returns an integer.
        """
        network = IP("%s" % (self.cidr))
        return int(network.len()-2)

    def _ips_assigned(self):
        """
            Make a set with already assigned IP-addresses in the network.

            Returns a set.
        """
        ips_char = set([interface.ip for interface in
            Interface.objects.filter(network=self).filter(ip__isnull=False)])
        
        #normalize IPv6 addressen through IPy: fill zeros, etc
        return map(lambda x: IP(x).strNormal(), ips_char)

    @property
    def netaddress(self):
        network = IP("%s" % (self.cidr))
        netaddress = network.net()
        return netaddress.strNormal()

    @property
    def netmask(self):
        network = IP("%s" % (self.cidr))
        netmask = network.netmask()
        return netmask.strNormal()

    def count_ips_assigned(self):
        """
            Count the amount of assigned IP-addresses in the network.

            Returns an integer.
        """
        return Interface.objects.filter(network=self).filter(ip__isnull=False).count()

    def count_ips_free(self):
        """
            Calculate the size of the pool of unassigned IP-addresses in the network.

            Returns an integer.
        """
        return self._max_hosts() - self.count_ips_assigned()

    def pick_ip(self):
        """
            Pick an IP-address in the network which hasn't been assigned yet.

            Returns a string.
        """
        assigned = self._ips_assigned()
        network = IP("%s" % (self.cidr))
        netaddress = network.net().ip
        broadcast = network.broadcast().ip
        poll_ip = netaddress + 1 # netaddress is in use already

        found = False
        while not found and poll_ip < broadcast:
            poll_ip_str = IP(poll_ip).strNormal()
            if poll_ip_str in assigned or poll_ip_str == IP(self.gateway).strNormal():
                poll_ip += 1
                continue
            found = True

        if found:
            ip = poll_ip_str
        else:
            logger.warning("No more IP's available in network '%s'"%self)
            ip = None

        return ip

    def default_gateway(self):
        """
            Return the first available ip address as the default gateway.
        """
        network = IP("%s" % (self.cidr) )
        return IP(network.ip+1).strNormal()

    # Deprecated
    #def construct_interface_label(self, machine):
    #    """
    #        Construct a label for an interface that's asking for it. The default
    #        label of an interface is based on info of its machine and network.
    #    """
    #    interface_label = self.hostnames.format(machine=machine)
    #    return interface_label

    def save(self, force_insert=False, force_update=False):
        if not self.gateway:
            self.gateway = self.default_gateway() 
        try:
            super(Network, self).save(force_insert, force_update)
        except IntegrityError, e:
            logger.error(e)


class Host(CMTModel):
    """
    """
    # Relations:
    domain = models.ForeignKey('Domain', blank=True, null=True)
    interface = models.ForeignKey('Interface', blank=True, null=True)

    # Fields:
    label = models.CharField(max_length=255, help_text='Short hostname')
    cnames = models.CharField(max_length=255, blank=True, null=True)
    primary = models.BooleanField()

    class Meta:
        ordering = ('label',)
    
    @property
    def fqdn(self):
        return '%s.%s' % (self.label, self.domain.label)

    def __unicode__(self):
        return unicode(self.label)


class Domain(CMTModel):
    """
    """
    # Fields:
    label = models.CharField(max_length=255)

    class Meta:
        ordering = ('label',)
    
    def __unicode__(self):
        return unicode(self.label)


class Entry(CMTModel):
    """
    """
    # Relations:
    entry_type = models.ForeignKey('EntryType')
    host = models.ForeignKey('Host', blank=True, null=True)
    network = models.ForeignKey('Network', blank=True, null=True)

    # Fields:
    label = models.CharField(max_length=255)

    class Meta:
        ordering = ('label',)

    def save(self, *args, **kwargs):
        if (self.host is None and self.network is None) or not (self.host is None or self.network is None):
            # So: both not set, or not one of both set
            raise ValidationError( "Error: either host or network has to be set" )
        super(Entry, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return unicode(self.label)


class EntryType(CMTModel):
    """
    """
    # Fields:
    label = models.CharField(max_length=255)

    class Meta:
        ordering = ('label',)
    
    def __unicode__(self):
        return unicode(self.label)


class Config(CMTModel):
    """
    """
    # Relations:
    config_type = models.ForeignKey('ConfigType')

    # Fields:
    label = models.CharField(max_length=255)

    class Meta:
        ordering = ('label',)
    
    def __unicode__(self):
        return unicode(self.label)


class ConfigType(CMTModel):
    """
    """
    # Fields:
    label = models.CharField(max_length=255, help_text="Kind of configuration, 'dhcp' or 'dns reverse' for example")

    class Meta:
        ordering = ('label',)
    
    def __unicode__(self):
        return unicode(self.label)



