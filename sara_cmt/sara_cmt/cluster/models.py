from django.db import models

from IPy import IP

from sara_cmt.logger import Logger
logger = Logger().getLogger()

from sara_cmt.django_cli import ModelExtension

from datetime import date



class MACAddressField(models.CharField):
  """
    Model field for a MAC-address, based on a CharField.
  """

  __metaclass__ = models.SubfieldBase

  def __init__(self, *args, **kwargs):
    kwargs['max_length'] = 17
    kwargs['unique'] = True
    super(MACAddressField, self).__init__(*args, **kwargs)

  def save(self, force_insert=False, force_update=False):
    # TODO: strip macaddress and check for uniqueness in case a macaddress is given

    super(MACAddressField, self).save(force_insert, force_update)


class Cluster(models.Model, ModelExtension):
  name = models.CharField(max_length=30, unique=True)
  note = models.TextField(blank=True)

  class Meta:
    ordering = ['name']


  def __unicode__(self):
    return self.name or None


class Location(models.Model, ModelExtension):
  """
    A class to hold information about the physical location of a model. In the
    case of CMTSARA it is a superclass of Site, ContactPerson and Company.
  """
  
  address1   = models.CharField(verbose_name='address', max_length=30)
  address2   = models.CharField(verbose_name='address', max_length=30, blank=True)
  postalcode = models.CharField(max_length=9, blank=True)
  city       = models.CharField(max_length=30)
  country    = models.CharField(max_length=30, blank=True)
  room       = models.CharField(max_length=30, blank=True)

  class Meta:
    abstract = True


  def __unicode__(self):
    return '%s, %s' % (country, postalcode)


class Site(Location):
  """
    A site is a physical location which houses a collection of racks. It can be
    a(n address of a) building, or more detailed a specific room in a building.
  """
  
  name = models.SlugField(max_length=30, editable=False, unique=True)
  note = models.TextField(blank=True)

  class Meta:
    ordering = ['country', 'city', 'address1']


  def __unicode__(self):
    return self.name

  def save(self, force_insert=False, force_update=False):
    if self.room:
      self.name = '%s - %s (%s)' % (self.city, self.address1, self.room)
    else:
      self.name = '%s - %s' % (self.city, self.address1)
    super(Site, self).save(force_insert, force_update)


class Company(Location):
  """
    The Company-model can be linked to hardware. This way you are able to define
    contactpersons for a specific piece of hardware.
  """
  
  name    = models.CharField(max_length=30)
  website = models.URLField(verify_exists=True)

  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'companies'


class Position(models.Model, ModelExtension):
  label = models.CharField(max_length=30, help_text="'Account Manager' for example")

  def __unicode__(self):
    return self.label


class Department(models.Model, ModelExtension):
  label = models.CharField(max_length=50, help_text="'High Performance Computing & Visualisation' for example")

  def __unicode__(self):
    return self.label


class Contact(Location):
  """
    Contactpersons can be linked to different sites, hardware, or its vendors.
    This makes it possible to lookup contactpersons in case of problems on a
    site or with specific hardware.
  """
  
  employer  = models.ForeignKey(Company, related_name='employees')
  department = models.ForeignKey(Department, related_name='employees', null=True, blank=True)
  position  = models.ForeignKey(Position, related_name='contacts')
  added_on  = models.DateField(editable=False, default=date.today)
  active    = models.BooleanField(editable=True, default=True)
  note      = models.TextField(default='', blank=True)
  
  firstname = models.CharField(verbose_name='first name', max_length=30)
  lastname  = models.CharField(verbose_name='last name', max_length=30)
  email     = models.EmailField()
  phone     = models.CharField(max_length=17)
  fax       = models.CharField(max_length=17, blank=True)

  def __unicode__(self):
    return self.fullname()

  def fullname(self):
    return '%s %s' % (self.firstname, self.lastname)

  class Meta:
    ordering = ('lastname', 'firstname')
    unique_together = ('firstname', 'lastname')


class Rack(models.Model, ModelExtension):
  """
    A Rack is a standardized system for mounting various HardwareUnits in a
    stack of slots. It is located on a site.
  """

  site     = models.ForeignKey(Site, verbose_name='is located at', related_name='racks')

  label    = models.SlugField(max_length=30)
  note     = models.TextField(default='', blank=True)
  capacity = models.PositiveIntegerField(verbose_name='number of slots')

  class Meta:
    ordering = ('site', 'label',)
    verbose_name = 'rack'
    verbose_name_plural = 'racks'


  # !!! TODO: Get rid of this !!!
  def __unicode__(self):
    try:
      assert self.label is not None, "rack hasn't got a label"
      return self.label
    except AssertionError, e:
      print AssertionError, e
      return '[None]'


class HardwareSpecifications(models.Model, ModelExtension):
  """
    The Model-model is being used to specify some extra information about a
    specific type (model) of hardware.
  """
  
  vendor         = models.ForeignKey(Company, related_name='model specifications')

  name           = models.CharField(max_length=30, unique=True)
  system_id      = models.CharField(max_length=30, blank=True)
  slots_size     = models.PositiveIntegerField(help_text='size in U for example')
  slots_capacity = models.PositiveIntegerField(default=0, help_text='capacity in U for example')
  
  class Meta:
    verbose_name_plural = 'hardware specifications'
    ordering = ('vendor', 'name')


  def __unicode__(self):
    return '%s (%s)' % (self.name, self.vendor)


class Warranty(models.Model, ModelExtension):
  """
    A class which contains warranty information of a (collection of) hardware.
  """

  label      = models.CharField(max_length=30, unique=True)
  date_from  = models.DateField(verbose_name='valid from')
  months     = models.PositiveIntegerField()
  date_to    = models.DateField(verbose_name='expires at', editable=False)

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
        month = (self.date_from.month + self.months) %12
      )
      super(Warranty, self).save(force_insert, force_update)
    except AttributeError, e:
      logger.error(e)


class Role(models.Model, ModelExtension):
  """
    This describes a possible role of a HardwareUnit in the cluster. A piece of
    hardware can have a role like 'switch', 'compute node', 'patchpanel', 'pdu',
    'admin node', 'login node', etc...
    Those roles can be used for all kinds of rules on HardwareUnits which exist
    in the cluster.
  """
  label = models.CharField(max_length=30, unique=True)
  note  = models.TextField(blank=True)

  class Meta:
    verbose_name = 'role'
    verbose_name_plural = 'roles'


  def __unicode__(self):
    return self.label



class HardwareUnit(models.Model, ModelExtension):
  cluster      = models.ForeignKey('Cluster', related_name='hardware')
  role         = models.ForeignKey('Role', related_name='hardware')
  networks     = models.ManyToManyField('Network', through='Interface')
  specifications = models.ForeignKey('HardwareSpecifications', null=True, blank=True, related_name='hardware')
  warranty     = models.ForeignKey('Warranty', null=True, blank=True, related_name='hardware')
  rack         = models.ForeignKey('Rack', related_name='contents')

  service_tag  = models.CharField(max_length=30, blank=True, unique=True)
  serialnumber = models.CharField(max_length=30, blank=True, unique=True)
  first_slot   = models.PositiveIntegerField()
  hostname     = models.CharField(max_length=30, blank=True)

  class Meta:
    verbose_name = "piece of hardware"
    verbose_name_plural = "hardware pieces"
    ordering = ['rack__label', 'first_slot']
    unique_together = [('rack', 'first_slot')]
    

  def __unicode__(self):
    try:
      assert self.hostname, "piece of hardware hasn't got a hostname yet"
      return self.hostname
    except AssertionError, e:
      return e
      
  def save(self, force_insert=False, force_update=False):
    """
      First check if the hostname has already been filled in. If it's still
      emtpy, then set it to the default basename (based on rack# and node#).
    """
    if not self.hostname:
      self.hostname = self.default_basename()

    super(HardwareUnit, self).save(force_insert, force_update)

  def default_basename(self):
    # TODO: make dynamic for different types of clusters
    try:
      assert self.rack.label is not None and self.first_slot is not None, 'not able to generate hostname'
      return 'r%sn%s' % (self.rack.label, self.first_slot)
    except:
      pass
    

class Network(models.Model, ModelExtension):
  """
    Class with information about a network. Networks are connected with
    Interfaces (and HardwareUnits as equipment through Interface).
  """
  equipment  = models.ManyToManyField('HardwareUnit', through='Interface')

  name       = models.CharField(max_length=30, help_text='example: infiniband')
  netaddress = models.IPAddressField(help_text='example: 192.168.1.0')
  netmask    = models.IPAddressField(help_text='example: 255.255.255.0')
  domain     = models.CharField(max_length=30, help_text='example: irc.sara.nl')
  prefix     = models.CharField(max_length=10, blank=True, help_text='example: ib-')

  class Meta:
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
    

class Interface(models.Model, ModelExtension):
  network   = models.ForeignKey('Network', related_name='interfaces')
  hardware  = models.ForeignKey('HardwareUnit', related_name='interfaces', verbose_name='machine')
  type      = models.ForeignKey('InterfaceType', related_name='interfaces', verbose_name='type')
  name      = models.CharField(max_length=30, blank=True, help_text='Automagically generated if kept empty') # TODO: Default name has to be based on the prefix of the network
  hwaddress = MACAddressField(null=True, blank=True, verbose_name='hardware address', help_text="6 Octets, optionally delimited by a space ' ', a hyphen '-', or a colon ':'.")
  ip        = models.IPAddressField(editable=False, null=True, blank=True)
  #extern_ip = models.IPAddressField(null=True, blank=True)

  def __unicode__(self):
    return self.name or 'anonymous'

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

      self.name = '%s%s' % (self.network.prefix, self.hardware.hostname)

      super(Interface, self).save(force_insert, force_update)
    except AssertionError, e:
      print AssertionError, e


class InterfaceType(models.Model, ModelExtension):
  label = models.CharField(max_length=30, help_text="'DRAC 4' for example")
  vendor = models.ForeignKey('Company', null=True, blank=True, related_name='interfaces')

  class Meta:
    verbose_name = 'type of interface'
    verbose_name_plural = 'types of interfaces'


  def __unicode__(self):
    return self.label
