from django.db import models

from IPy import IP

from sara_cmt.logger import Logger
logger = Logger().getLogger()

from sara_cmt.django_cli import ModelExtension

from tagging.fields import TagField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from sara_cmt import settings


# !!! TODO: classes for templates !!!




######
#
# Classes of sara_cmt.core
#
class Cluster(ModelExtension):
  name = models.CharField(max_length=30, unique=True)

  class Meta:
    ordering = ['name']

  def __unicode__(self):
    return self.name or None


#try:
#  tagging.register(Cluster)
#except tagging.AlreadyRegistered:
#  logger.debug('Cluster has already been registered')
#  pass



class HardwareUnit(ModelExtension):
  cluster      = models.ForeignKey('Cluster', related_name='hardware')
  role         = models.ManyToManyField('Role', related_name='hardware')
  networks     = models.ManyToManyField('Network', related_name='hardware', through='Interface')
  specifications = models.ForeignKey('HardwareModel', related_name='hardware', null=True, blank=True)
  warranty     = models.ForeignKey('WarrantyContract', related_name='hardware', null=True, blank=True)
  rack         = models.ForeignKey('Rack', related_name='contents')

  serialnumber = models.CharField(max_length=30, blank=True, null=True, unique=True) # should be a field of Specifications
  service_tag  = models.CharField(max_length=30, blank=True, null=True, unique=True)
  first_slot   = models.PositiveIntegerField()
  label        = models.CharField(max_length=30, blank=True)

  class Meta:
    #verbose_name = "piece of hardware"
    verbose_name_plural = "hardware"
    ordering = ['cluster__name', 'rack__label', 'first_slot']
    unique_together = [('rack', 'first_slot')]

  def _address(self):
    return self.rack.address
  address = property(_address)

  def __unicode__(self):
    try:
      assert self.label, "piece of hardware hasn't got a label yet"
      return self.label
    except AssertionError, e:
      return e
      
  def save(self, force_insert=False, force_update=False):
    """
      First check if the label has already been filled in. If it's still empty,
      then set it to the default basename (based on rack# and node#).
    """
    if not self.label:
      self.label = self.default_label()

    super(HardwareUnit, self).save(force_insert, force_update)

  def default_label(self):
    # TODO: make dynamic for different types of clusters
    try:
      assert self.rack.label is not None and self.first_slot is not None, 'not able to generate a label'
      return 'r%sn%s' % (self.rack.label, self.first_slot)
    except:
      pass
    

class Interface(ModelExtension):
  network   = models.ForeignKey('Network', related_name='interfaces')
  hardware  = models.ForeignKey('HardwareUnit', related_name='interfaces', verbose_name='machine') # ??? host ???
  type      = models.ForeignKey('InterfaceType', related_name='interfaces', verbose_name='type')
  hostname  = models.CharField(max_length=30, blank=True, help_text='Automagically generated if kept empty') # TODO: Default name has to be based on the prefix of the network
  hwaddress = models.CharField(max_length=17, blank=True, verbose_name='hardware address', help_text="6 Octets, optionally delimited by a space ' ', a hyphen '-', or a colon ':'.", unique=True)
  ip        = models.IPAddressField(editable=False, null=True, blank=True)


  def __unicode__(self):
    return self.hostname or 'anonymous'

  def save(self, force_insert=False, force_update=False):
    """
      First check for a correct IP address before saving the object. 
      Pick a new one in the related network when the IP hasn't been set yet, or
      when the network has been changed.
    """
    try:
      assert isinstance(self.network, Network), "network doesn't exist"

      ip = IP(self.ip or 0)
      try:
        network = IP('%s/%s' % (self.network.netaddress, self.network.netmask))
      except ValueError, e:
        print ValueError, e

      # Pick a new IP when it's not defined yet or when the network has been changed
      if ip not in network:
        self.ip = self.network.pick_ip()

      self.hostname = '%s%s' % (self.network.prefix, self.hardware.label)

      super(Interface, self).save(force_insert, force_update)
    except AssertionError, e:
      print AssertionError, e
    

class Network(ModelExtension):
  """
    Class with information about a network. Networks are connected with
    Interfaces (and HardwareUnits as equipment through Interface).
  """
  equipment  = models.ManyToManyField('HardwareUnit', through='Interface')

  name       = models.CharField(max_length=30, help_text='example: infiniband')
  netaddress = models.IPAddressField(help_text='example: 192.168.1.0')
  netmask    = models.IPAddressField(help_text='example: 255.255.255.0')
  domain     = models.CharField(max_length=30, help_text='example: irc.sara.nl')
  vlan       = models.PositiveIntegerField(max_length=3, null=True, blank=True)
  prefix     = models.CharField(max_length=10, blank=True, help_text='example: ib-')

  class Meta:
    ordering = ('name', 'domain',)
    verbose_name = 'network'
    verbose_name_plural = 'networks'

  def __unicode__(self):
    return self.name

  def _max_hosts(self):
    """
      Give the total amount of IP-addresses which could be assigned to hosts in
      this network.

      Returns an integer.
    """
    network = IP("%s/%s" % (self.netaddress, self.netmask))
    return int(network.len()-2)

  def _ips_assigned(self):
    """
      Make a set with already assigned IP-addresses in the network.

      Returns a set.
    """
    return set(
      [interface.ip for interface in Interface.objects.filter(network=self).filter(ip__isnull=False)]
    )

  def count_ips_assigned(self):
    """
      Count the amount of assigned IP-addresses in the network.

      Returns an integer.
    """
    return len(self._ips_assigned())

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
    network = IP("%s/%s" % (self.netaddress, self.netmask))
    netaddress = network.net().ip
    broadcast = network.broadcast().ip
    poll_ip = netaddress+1 # netaddress is in use already

    found = False
    while not found and poll_ip < broadcast:
      if IP(poll_ip).strNormal() in  assigned:
        poll_ip += 1
        continue
      found = True
    
    if found:
      ip = IP(poll_ip).strNormal()
    else:
      ip = None
      print "WARNING: No more IP's available in network '%s'" % self

    return ip

  def cidr(self):
    network = IP("%s/%s" % (self.netaddress, self.netmask))
    return network.strNormal()


class Rack(ModelExtension):
  """
    A Rack is a standardized system for mounting various HardwareUnits in a
    stack of slots. It is located on a site.
  """

  room = models.ForeignKey('Room', related_name='racks')

  label    = models.SlugField(max_length=30)
  capacity = models.PositiveIntegerField(verbose_name='number of slots')


  class Meta:
    ordering = ('room', 'label',)
    verbose_name = 'rack'
    verbose_name_plural = 'racks'


  def _address(self):
    return self.room.address
  address = property(_address)


  def __unicode__(self):
    return 'rack %s'%(self.label)

#
#
#
######



######
#
# Classes for sara_cmt.locations
#

class Country(ModelExtension):
  name         = models.CharField(max_length=30, unique=True)
  country_code = models.PositiveIntegerField(help_text='''Example: In case of The Netherlands it's 31''')
  # Country codes can be found on:
  #   http://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.164D-2009-PDF-E.pdf

  class Meta:
    unique_together = ('name', 'country_code')
    verbose_name_plural = 'countries'


  def __unicode__(self):
    return self.name


class Address(ModelExtension):
  """
    A class to hold information about the physical location of a model. In the
    case of CMTSARA it is a superclass of Site, ContactPerson and Company.
  """
  
  country    = models.ForeignKey(Country, null=True, blank=True, related_name='addresses')
  address    = models.CharField(max_length=60)
  postalcode = models.CharField(max_length=9, blank=True)
  city       = models.CharField(max_length=30)

  def _companies(self):
    return ' | '.join([comp.name for comp in self._companies.all()]) or '-'
  companies = property(_companies)

  class Meta:
    unique_together = ('address', 'city')
    verbose_name_plural = 'addresses'


  def __unicode__(self):
    return '%s - %s' % (self.city, self.address)


class Room(ModelExtension):
  address = models.ForeignKey(Address, related_name='rooms')

  floor   = models.IntegerField(max_length=2)
  label   = models.CharField(max_length=30, blank=False)

  class Meta:
    unique_together = ('address', 'floor', 'label')
    
  def __unicode__(self):
    #return unicode('%s - %s'%(self.address,self.label))
    return self.label


# ??? What todo with this model ???
class Site(ModelExtension):
  """
  """
  name = models.CharField(max_length=30, unique=True)

  def __unicode__(self):
    return self.name

#
#
#
######


######
#
# Classes for sara_cmt.contacts
#

class Company(ModelExtension):
  """
    The Company-model can be linked to hardware. This way you are able to define
    contactpersons for a specific piece of hardware.
  """
  
  addresses = models.ManyToManyField(Address, related_name='_companies')

  #type    = models.ChoiceField() # !!! TODO: add choices like vendor / support / partner / etc... !!!
  name    = models.CharField(max_length=64)
  website = models.URLField()

  def get_addresses(self):
    return ' | '.join([address.address for address in self.addresses.all()]) or '-'

  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'companies'


class Connection(ModelExtension):
  """
    Contacts can be linked to different sites, hardware, or its vendors.
    This makes it possible to lookup contactpersons in case of problems on a
    site or with specific hardware.
  """
  address = models.ForeignKey(Address, related_name='connections')
  company = models.ForeignKey(Company, related_name='companies')

  active = models.BooleanField(editable=True, default=True)
  name   = models.CharField(verbose_name='full name', max_length=60)
  email  = models.EmailField(blank=True, null=True)

  def __unicode__(self):
    return self.name
    #return self.fullname()

  #def _lastname(self):
  #  return name.split()[-1]
  #lastname = property(_lastname)

  def _address(self):
    return address.address

  class Meta:
    #ordering = ('lastname',)
    verbose_name = 'contact'
    unique_together = ('company', 'name')


class Telephonenumber(ModelExtension):
  NUMBER_CHOICES = (
    ('T', 'Telephone'),
    ('C', 'Cellphone'),
    ('F', 'Fax')
  )
  country      = models.ForeignKey(Country, related_name='telephone_numbers')
  connection = models.ForeignKey(Connection, blank=False, null=False, related_name='telephone_numbers')
  areacode          = models.CharField(max_length=4) # because it can start with a zero
  subscriber_number = models.IntegerField(verbose_name='number', max_length=15)
  type = models.CharField(max_length=1, choices=NUMBER_CHOICES)

  # !!! TODO: link to company / contact / etc... !!!

  def __unicode__(self):
    return '+%i(%s)%s-%i' % (self.country.country_code, self.areacode[:1], self.areacode[1:], self.subscriber_number)

  class Meta:
    ordering = ('connection',)


#
#
#
#####


######
#
# Classes for sara_cmt.specifications
#


class HardwareModel(ModelExtension):
  """
    The Model-model is being used to specify some extra information about a
    specific type (model) of hardware.
  """
  vendor = models.ForeignKey(Company, related_name='model specifications')

  name       = models.CharField(max_length=30, unique=True)
  #model_id   = models.CharField(max_length=30, blank=True)
  rackspace  = models.PositiveIntegerField(help_text='size in U for example')
  expansions = models.PositiveIntegerField(default=0, help_text='number of expansion slots')
  
  class Meta:
    verbose_name = 'model'
    #verbose_name_plural = 'specifications'
    ordering = ('vendor', 'name')


  def __unicode__(self):
    return '%s (%s)' % (self.name, self.vendor)


class Role(ModelExtension):
  """
    This describes a possible role of a HardwareUnit in the cluster. A piece of
    hardware can have a role like 'switch', 'compute node', 'patchpanel', 'pdu',
    'admin node', 'login node', etc...
    Those roles can be used for all kinds of rules on HardwareUnits which exist
    in the cluster.
  """
  label = models.CharField(max_length=30, unique=True)


  class Meta:
    ordering = ['label']
    verbose_name = ('role')
    verbose_name_plural = 'roles'


  def __unicode__(self):
    return self.label


class InterfaceType(ModelExtension):
  label = models.CharField(max_length=60, help_text="'DRAC 4' for example")
  # ??? TODO: add a CharField for version ???
  vendor = models.ForeignKey('Company', null=True, blank=True, related_name='interfaces')


  class Meta:
    ordering = ['label']
    verbose_name = 'type of interface'
    verbose_name_plural = 'types of interfaces'


  def __unicode__(self):
    return self.label

#
#
#
######


######
#
# Classes for sara_cmt.support
#

class WarrantyType(ModelExtension):
  """
A type of warranty offered by a company.
  """
  contact = models.ForeignKey(Connection, related_name='warranty types')

  label = models.CharField(max_length=30, unique=True)

  def __unicode__(self):
    return self.label


class WarrantyContract(ModelExtension):
  """
    A class which contains warranty information of (a collection of) hardware.
  """
  type = models.ForeignKey(WarrantyType, blank=True, null=True, related_name='contracts')

  label       = models.CharField(max_length=30, unique=True)
  date_from   = models.DateField(verbose_name='valid from')
  months      = models.PositiveIntegerField()
  date_to     = models.DateField(verbose_name='expires at', editable=False)


  class Meta:
    verbose_name_plural = 'warranties'


  def __unicode__(self):
    return self.label

  def save(self, force_insert=False, force_update=False):
    """
      Before saving to the database, the date of expiration has to be calculated.
    """
    try:
      self.date_to = self.date_from.replace(
        year = self.date_from.year + (self.date_from.month-1 + self.months) / 12,
        month = (self.date_from.month + self.months) % 12
      )
      super(WarrantyContract, self).save(force_insert, force_update)
    except AttributeError, e:
      logger.error(e)
