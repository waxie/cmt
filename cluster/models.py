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

import re
import logging
from datetime import date

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from psycopg2 import IntegrityError

from IPy import IP

from cmt.extensions import ModelExtension

logger = logging.getLogger('cmt.cluster.models')


class Cluster(ModelExtension):
    """
        A labeled group of hardware pieces.
    """
    re_valid_machines = re.compile(r'^([a-z0-9\{]{1})([a-z0-9\-\_\{\}]{1,61})([a-z0-9\}]{1})$')
    machines_validator = RegexValidator(
        re_valid_machines,
        'Enter a valid machinenames stringformat. Example: r{rack}n{first_slot}. Valid characters: [0-9], [a-z], "{", "}" and "-"','invalid'
    )

    name = models.CharField(max_length=255, unique=True)
    machinenames = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='''stringformat of machine names in the cluster, example: 'r{rack}n{first_slot}''',
        validators=[machines_validator]
    )

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.name) or None


class Equipment(ModelExtension):
    """
        A specific piece of hardware.
    """
    STATE_CHOICES = (
        ('new', 'new'),
        ('clean', 'clean'),
        ('configured', 'configured'),
        ('unknown', 'unknown'),
        ('off', 'off'))
        
    cluster = models.ForeignKey('Cluster', related_name='hardware')
    role = models.ManyToManyField('Role', related_name='hardware')
    network = models.ManyToManyField('Network', related_name='hardware', through='Interface')
    specifications = models.ForeignKey('HardwareModel', related_name='hardware', null=True, blank=True)
    warranty = models.ForeignKey('WarrantyContract', related_name='hardware', null=True, blank=True)
    rack = models.ForeignKey('Rack', related_name='contents')
    seller = models.ForeignKey('Connection', related_name='sold', null=True, blank=True)
    owner = models.ForeignKey('Connection', related_name='owns', null=True, blank=True)
    state = models.CharField(max_length=10, null=True, blank=True, choices=STATE_CHOICES, default='unknown')
    warranty_tag = models.CharField(max_length=255, blank=True, null=True, help_text='Service tag', unique=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True, unique=True)
    first_slot = models.PositiveIntegerField(blank=True, null=True)
    label = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "equipment"
        # ordering = ('cluster__name', 'rack__label', 'first_slot')
        ordering = ('rack__label', 'first_slot')
        unique_together = (('rack', 'first_slot'), ('cluster', 'label'))

    @property
    def address(self):
        return self.rack.address

    @property
    def room(self):
        return self.rack.room

    @property
    def roles(self):
        return [str(role.label) for role in self.role.all()]

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
        if not self.warranty_tag:
            self.warranty_tag = None
        if not self.serial_number:
            self.serial_number = None
        if not self.first_slot:
            self.first_slot = None

        super(Equipment, self).save(force_insert, force_update)

    def default_label(self):
        try:
            assert self.rack.label is not None and self.first_slot is not \
                None, 'not able to generate a label'

            if self.cluster.machinenames is not None and self.cluster.machinenames != '':
                machine_label = self.cluster.machinenames.format( rack=self.rack.label, first_slot=self.first_slot )
            else:
                # RB: fail back to previous default behaviour
                machine_label = 'r%sn%s' %(self.rack.label, self.first_slot)

            assert machine_label.find( '{' ) == -1, \
                'unable to format cluster machine name: %s' %machine_label

            return machine_label
        except:
            pass


class Interface(ModelExtension):
    """
        An interface of a piece of hardware.
    """
    re_valid_mac = re.compile(r'([A-Fa-f\d]{2}[:-]?){5}[A-Fa-f\d]{2}')
    re_mac_octets = re.compile(r'[A-Fa-f\d]{2}')
    re_valid_cnames  = re.compile(r'^[a-z\d\-\.]+([,]{1}[a-z\d\-\.]+)*$')

    # valid hostname  = 1-63 length, lowercase, numbers and hyphen (-). May not begin/end with hyphen
    re_valid_hostname = re.compile(r'^([0-9a-z]{1,2})$|^([a-z0-9]{1})([a-z0-9\-]{1,61})([a-z0-9]{1})$')

    hwaddress_validator = RegexValidator(
        re_valid_mac,
        'Enter a valid MAC address. Example: "cc:cc:cc:cc:cc:cc". Valid characters: [a-f], [A-F], [0-9] and ":"', 'invalid'
    )
    cnames_validator = RegexValidator(
        re_valid_cnames,
        'One or more (comma seperated, no spaces) aliases. Example: "test,test.console,alias2". Valid characters: [a-z], [0-9], "-", "." and ","', 'invalid'
    )
    hostname_validator = RegexValidator(
        re_valid_hostname,
        'Enter a valid hostname. Example: "myhostname-rack2node3". Valid characters: [a-z], [0-9] and "-"','invalid'
    )

    network = models.ForeignKey('Network', related_name='interfaces')
    host = models.ForeignKey('Equipment', related_name='interfaces', verbose_name='machine')
    iftype = models.ForeignKey('InterfaceType', related_name='interfaces', verbose_name='type')
    label = models.CharField(max_length=255, help_text='Automagically generated if kept empty', validators=[hostname_validator])
    aliases = models.CharField(max_length=255, help_text='Cnames comma-seperated', blank=True, null=True, validators=[cnames_validator])

    hwaddress = models.CharField(max_length=17, blank=True, null=True, verbose_name='hardware address', help_text="6 Octets, optionally delimited by a space ' ', a hyphen '-', or a colon ':'.", validators=[hwaddress_validator])
    ip = models.GenericIPAddressField(blank=True, null=True, protocol='both')

    class Meta:
        unique_together = ('network', 'hwaddress')
        ordering = ('host__cluster__name', 'host__rack__label', 'host__first_slot')

    @property
    def fqdn(self):
        return '%s.%s' % (self.label, self.network.domain)

    @property
    def cnames(self):
        if self.aliases:
            return self.aliases.split(',')

    @property
    def api_slug_field(self):
        return {
            'label': self.label,
            'fqdn': self.fqdn,
            'ip': self.ip,
            'network': self.network.name,
            'iftype': self.iftype.label
        }

    def __unicode__(self):
        # return self.fqdn
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
            # assert isinstance(self.network, Network), "network doesn't exist"

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


class Network(ModelExtension):
    """
        Class with information about a network. Networks are connected with
        Interfaces (and Equipments as equipment through Interface).
    """
    re_valid_domain = re.compile(r'^(^(?:[a-z0-9]{1}[a-z0-9\-]{1,61}[a-z0-9]{1}\.?)+(?:[a-z]{2,})$)')
    domain_validator = RegexValidator(re_valid_domain,'Enter a valid domain. Example: admin1.my-domain.com. Valid characters: [a-z], [0-9], "." and "-"','invalid')
    re_valid_hosts = re.compile(r'^([0-9a-z]{1,2})$|^([a-z0-9\{]{1})([a-z0-9\-\{\}]{1,61})([a-z0-9\}]{1})$')
    hosts_validator = RegexValidator(re_valid_hosts,'Enter a valid hostnames stringformat. Example: ib-{machine}. Valid characters: [a-z], [0-9], "{", "}" and "-"','invalid')
    name = models.CharField(max_length=255, help_text='example: infiniband')
    cidr = models.CharField(max_length=100, help_text='example: 192.168.1.0/24 or fd47:e249:06b2:0385::/64')
    gateway = models.GenericIPAddressField(blank=True, help_text='Automagically generated if kept empty', null=True)
    domain = models.CharField(max_length=255, help_text='example: irc.sara.nl', validators=[domain_validator])
    vlan = models.PositiveIntegerField(null=True, blank=True)
    hostnames = models.CharField(max_length=255, help_text='''stringformat of hostnames in the network, example: 'ib-{machine}''', validators=[hosts_validator])

    class Meta:
        ordering = ('name', 'domain')
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
        
        # normalize IPv6 addressen through IPy: fill zeros, files
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

    def construct_interface_label(self, machine):
        """
            Construct a label for an interface that's asking for it. The default
            label of an interface is based on info of its machine and network.
        """
        interface_label = self.hostnames.format(machine=machine)
        return interface_label

    def save(self, force_insert=False, force_update=False):
        if not self.gateway:
            self.gateway = self.default_gateway() 
        try:
            super(Network, self).save(force_insert, force_update)
        except IntegrityError, e:
            logger.error(e)


class Rack(ModelExtension):
    """
        A Rack is a standardized system for mounting various Equipments in a
        stack of slots.
    """

    room = models.ForeignKey('Room', related_name='racks')
    label = models.SlugField(max_length=255)
    capacity = models.PositiveIntegerField(verbose_name='number of slots')

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


class Country(ModelExtension):
    """
        Model for country - country-code pairs. Country-codes can be found on:
            http://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.164D-2009-PDF-E.pdf
    """
    name = models.CharField(max_length=255, unique=True)
    country_code = models.PositiveIntegerField(unique=True, help_text='''Example: In case of The Netherlands it's 31''')

    class Meta:
        verbose_name_plural = 'countries'
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.name)


class Address(ModelExtension):
    """
        A class to hold information about the physical location of a model.
    """
    country = models.ForeignKey(Country, null=True, blank=True, related_name='addresses')
    address = models.CharField(max_length=255)
    postalcode = models.CharField(max_length=9, blank=True)
    city = models.CharField(max_length=255)

    @property
    def companies(self):
        return ' | '.join([comp.name for comp in self._companies.all()]) or '-'

    class Meta:
        unique_together = ('address', 'city')
        verbose_name_plural = 'addresses'
        ordering = ('postalcode',)

    def __unicode__(self):
        return unicode('%s - %s' % (self.city, self.address))


class Room(ModelExtension):
    """
        A room is located at an address. This is where racks of hardware can be
        found.
    """
    address = models.ForeignKey(Address, related_name='rooms')

    floor = models.IntegerField()
    label = models.CharField(max_length=255, blank=False)

    class Meta:
        unique_together = ('address', 'floor', 'label')
        ordering = ('address__postalcode', 'floor')

    def __unicode__(self):
        # return unicode('%s - %s'%(self.address,self.label))
        return unicode('%s (%s, %s)' % (self.label, self.address.address, self.address.city))


class Company(ModelExtension):
    """
        The Company-model can be linked to hardware. This way you are able to define
        contactpersons for a specific piece of hardware.
    """

    addresses = models.ManyToManyField(Address, related_name='_companies')

    #type = models.ChoiceField() # !!! TODO: add choices like vendor / support / partner / customer / files... !!!
    name = models.CharField(max_length=255)
    website = models.URLField()

    def get_addresses(self):
        return ' | '.join([address.address for address in self.addresses.all()]) or '-'

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'companies'
        ordering = ('name',) 


class Connection(ModelExtension):
    """
        Contacts can be linked to different sites, hardware, or its vendors.
        This makes it possible to lookup contactpersons in case of problems on a
        site or with specific hardware.
    """
    address = models.ForeignKey(Address, blank=True, null=True, related_name='connections')
    company = models.ForeignKey(Company, related_name='companies')

    active = models.BooleanField(editable=True, default=True)
    name = models.CharField(verbose_name='full name', max_length=255)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

    def _address(self):
        return address.address

    class Meta:
        verbose_name = 'contact'
        unique_together = ('company', 'name')
        ordering = ('company', 'address')


class Telephonenumber(ModelExtension):
    """
        Telephonenumber to link to a contact. Split in country-, area- and
        subscriber-part for easy filtering.
    """
    NUMBER_CHOICES = (
        ('T', 'Telephone'),
        ('C', 'Cellphone'),
        ('F', 'Fax'))
    country = models.ForeignKey(Country, related_name='telephone_numbers')
    connection = models.ForeignKey(Connection, blank=False, null=False, related_name='telephone_numbers')
    areacode = models.CharField(max_length=4) # because it can start with a zero
    subscriber_number = models.IntegerField(verbose_name='number')
    number_type = models.CharField(max_length=1, choices=NUMBER_CHOICES)

    # !!! TODO: link to company / contact / files... !!!

    def __unicode__(self):
        return unicode('+%i(%s)%s-%i' % (self.country.country_code, self.areacode[:1], self.areacode[1:], self.subscriber_number))

    class Meta:
        ordering = ('connection',)


class HardwareModel(ModelExtension):
    """
        This model is being used to specify some extra information about a
        specific type (model) of hardware.
    """
    vendor = models.ForeignKey(Company, related_name='hardware')
    name = models.CharField(max_length=255, unique=True)
    vendorcode = models.CharField(max_length=255, blank=True, null=True, unique=True, help_text='example: CISCO7606-S')
    rackspace = models.PositiveIntegerField(help_text='size in U for example')
    expansions = models.PositiveIntegerField(default=0, help_text='number of expansion slots')

    @property
    def api_slug_field(self):
        return self.__unicode__()

    class Meta:
        verbose_name = 'model'
        ordering = ('vendor', 'name')

    def __unicode__(self):
        return unicode('%s (%s)' % (self.name, self.vendor))

    def save(self, force_insert=False, force_update=False):
        """
            Be sure to save vendorcode as None, when kept blank.
        """
        if not self.vendorcode:
            self.vendorcode = None

        super(HardwareModel, self).save(force_insert, force_update)


class Role(ModelExtension):
    """
        This describes a possible role of a Equipment in the cluster. A piece of
        hardware can have a role like 'switch', 'compute node', 'patchpanel', 'pdu',
        'admin node', 'login node', files...
        Those roles can be used for all kinds of rules on Equipments which exist
        in the cluster.
    """
    label = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('label',)
        verbose_name = 'role'
        verbose_name_plural = 'roles'

    def __unicode__(self):
        return unicode(self.label)


class InterfaceType(ModelExtension):
    """
        Contains information about different types of interfaces.
    """
    vendor = models.ForeignKey('Company', null=True, blank=True, related_name='interfaces')
    label = models.CharField(max_length=255, help_text="'DRAC 4' for example")

    class Meta:
        # Note in docs of Model Meta options,
        # see http://docs.djangoproject.com/en/dev/ref/models/options/#ordering
        # "Regardless of how many fields are in ordering, the admin site uses
        # only the first field."
        # ordering = ('vendor', 'label')
        ordering = ('label',)
        verbose_name = 'type of interface'
        verbose_name_plural = 'types of interfaces'

    def __unicode__(self):
        return self.label


class WarrantyType(ModelExtension):
    """
        A type of warranty offered by a company.
    """
    contact = models.ForeignKey(Connection, related_name='warranty')
    label = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('contact__company__name', 'label')
    def __unicode__(self):
        return unicode(self.label)


class WarrantyContract(ModelExtension):
    """
        A class which contains warranty information of (a collection of) hardware. (SLA)
    """
    warranty_type = models.ForeignKey(WarrantyType, blank=True, null=True, related_name='contracts')

    contract_number = models.CharField(max_length=255, blank=True, null=True, unique=True, help_text='NSEN420201')
    annual_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text='433.61')
    label = models.CharField(max_length=255, unique=True)
    date_from = models.DateField(verbose_name='valid from')
    date_to = models.DateField(verbose_name='expires at')
    date_to.in_support_filter = True

    class Meta:
        ordering = ('label',)

    @property
    def expired(self):
        return self.date_to < date.today()

    @property
    def api_slug_field(self):
        return self.__unicode__()

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

        super(WarrantyContract, self).save(force_insert, force_update)
