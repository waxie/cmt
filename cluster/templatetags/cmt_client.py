#
# This file is part of CMT
#
# CMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# CMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMT.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2017 SURFsara

import sys
import string

# Inspired by Django tips on:
#   http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/
from django import template
from django.template.defaultfilters import stringfilter
from django.apps import apps
from django.db.models import QuerySet

from api.views import *
from api.filters import *

#from server.logger import Logger
#logger = Logger().getLogger()


register = template.Library()

class NoBlankLinesNode(template.Node):
    """
        Renderer that'll remove all blank lines.
    """

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return re.sub('\n([\ \t]*\n)+', '\n', force_unicode(
            self.nodelist.render(context)))

@register.tag
def noblanklines(parser, token):
    nodelist = parser.parse(('endnoblanklines',))
    parser.delete_first_token()
    return NoBlankLinesNode(nodelist)

@register.filter(is_safe=False)
def is_ipv4(value):

    try:
        if IP( value ).version() == 4:

            return True
    except ValueError:
        return False

    return False

@register.filter(is_safe=False)
def is_ipv6(value):

    try:
        if IP( value ).version() == 6:

            return True
    except ValueError:
        return False

    return False

@register.filter('cmt_startswith')
def cmt_startswith(text, starts):
    if isinstance(text, basestring):
        return text.startswith(starts)
    return False

@register.filter('ip6_reverse_address')
def ip6_reverse_address(address, network):
    _net = IP(network).reverseName()
    _address = IP(address).reverseName()
    length = (len(_address) - len(_net)) - 1
    return _address[0:length]

@stringfilter
def arpanize(value):
    """
        Converts a IPv4 (range) to reversed DNS style arpa notation

        Usage:
            {{{ <variable>|arpanize }}}

        I.e.:
            {% assign broadcast = '192.168.1.0' %}
            {{{ broastcast|arpanize }}}
        Results in output:
            1.168.192.in-addr.arpa
    """
    # deprecate me: use reverse_name

    try:
        ip = IP( value )

    except ValueError:

        return ''

    if ip.version() == 4:

        ip_blocks = value.split('.')

        reverse_block = [ ip_blocks[2], ip_blocks[1], ip_blocks[0], 'in-addr.arpa' ]

    elif ip.version() == 6:

        print 'FATAL ERROR: arpanize: does not support IPv6 address(es): %s' %( value )
        sys.exit(1)

    return string.join( reverse_block, '.' )

register.filter( 'arpanize', arpanize )

@stringfilter
def base_net(value):
    """
        Converts a IPv4 (range) to it's first 3 octects

        Usage:
            {{{ <variable>|base_net }}}

        I.e.:
            {% assign broadcast = '192.168.1.0' %}
            {{{ broastcast|base_net }}}
        Results in output:
            192.168.1
    """

    try:
        ip = IP( value )

    except ValueError:

        return ''

    if ip.version() == 4:

        ip_blocks = IP( value ).net().strNormal().split('.')
        base_net  = string.join( ip_blocks[:3], '.' )

    elif ip.version() == 6:

        print 'FATAL ERROR: base_net: does not support IPv6 address(es): %s' %( value )
        sys.exit(1)

    return string.join( ip_blocks[:3], '.' )

register.filter( 'base_net', base_net )

@stringfilter
def ip_last_digit(value):
    """
        Return's a IP's last digit

        Usage:
            {{{ <variable>|ip_last_digit }}}

        I.e.:
            {% assign myip4 = '192.168.1.123' %}
            {% assign myip6 = 'fd6b:be97:63d8:749f::123' %}
            ip4 last digit = {{{ myip4|ip_last_digit }}}
            ip6 last digit {{{ myip6|ip_last_digit }}}
        Results in output:
            ip4 last digit = 123
            ip6 last digit = 123
    """
    try:
        ip = IP( value )

    except ValueError:

        return ''

    if ip.version() == 4:

        split_char = '.'

    elif ip.version() == 6:

        split_char = ':'

    ip_blocks = IP( value ).strNormal().split( split_char )

    return ip_blocks[-1]
register.filter( 'ip_last_digit', ip_last_digit )


@stringfilter
def reverse_name(value):
    """
        Return's a IP or CIDR reverse (arpa) name

        Usage:
            {{{ <variable>|reverse_name}}}

        I.e.:
            {% assign ip4cidr24 = '192.168.1.0/24' %}
            ip4cidr/24 = {{{ ip4cidr24 }}}
            ip4cidr/24 reverse name = {{{ ip4cidr24|reverse_name }}}

            {% assign ip4cidr30 = '192.168.1.0/28' %}
            ip4cidr/30 = {{{ ip4cidr30 }}}
            ip4cidr/30 reverse name = {{{ ip4cidr30|reverse_name }}}

            {% assign ip4 = '192.168.1.123' %}
            ip4 = {{{ ip4 }}}
            ip4 reverse name = {{{ ip4|reverse_name }}}

            {% assign ip6cidr64 = 'fd93:59ef:8ce1:aac8::/64' %}
            ip6cidr/64 = {{{ ip6cidr64 }}}
            ip6cidr/64 reverse name  = {{{ ip6cidr64|reverse_name }}}

            {% assign ip6cidr76 = 'fd93:59ef:8ce1:aac8::/76' %}
            ip6cidr/76 = {{{ ip6cidr76 }}}
            ip6cidr/76 reverse name  = {{{ ip6cidr76|reverse_name }}}

            {% assign ip6 = 'fd93:59ef:8ce1:aac8::123' %}
            ip6 = {{{ ip6 }}}
            ip6 reverse name  = {{{ ip6|reverse_name }}}

        Results in output:
            ip4cidr/24 = 192.168.1.0/24
            ip4cidr/24 reverse name = 1.168.192.in-addr.arpa.

            ip4cidr/30 = 192.168.1.0/30
            ip4cidr/30 reverse name = 0-3.1.168.192.in-addr.arpa.

            ip4 = 192.168.1.123
            ip4 reverse name = 123.1.168.192.in-addr.arpa.

            ip6cidr/64 = fd93:59ef:8ce1:aac8::/64
            ip6cidr/64 reverse name = 8.c.a.a.1.e.c.8.f.e.9.5.3.9.d.f.ip6.arpa.

            ip6cidr/76 = fd93:59ef:8ce1:aac8::/76
            ip6cidr/76 reverse name = 0.0.0.8.c.a.a.1.e.c.8.f.e.9.5.3.9.d.f.ip6.arpa.

            ip6 = fd93:59ef:8ce1:aac8::123
            ip6 reverse name = 3.2.1.0.0.0.0.0.0.0.0.0.0.0.0.0.8.c.a.a.1.e.c.8.f.e.9.5.3.9.d.f.ip6.arpa.
    """
    try:
        ip = IP( value )
        return ip.reverseName()

    except ValueError:

        return ''

register.filter( 'reverse_name', reverse_name )

@stringfilter
def reverse_names(value):
    """
        Return's a CIDR reverse (arpa) names

        Usage:
            {{{ <variable>|reverse_names}}}

        I.e.:
            {% assign ip4cidr24 = '192.168.1.0/24' %}
            ip4cidr/24 = {{{ ip4cidr24 }}}
            ip4cidr/24 reverse names = {{{ ip4cidr24|reverse_names }}}

            {% assign ip4cidr30 = '192.168.1.0/30' %}
            ip4cidr/30 = {{{ ip4cidr30 }}}
            ip4cidr/30 reverse names = {{{ ip4cidr30|reverse_names }}}

            {% assign ip6cidr64 = 'fd93:59ef:8ce1:aac8::/64' %}
            ip6cidr/64 reverse names  = {{{ ip6cidr64|reverse_names }}}

        Results in output:
            ip4cidr/24 = 192.168.1.0/24
            ip4cidr/24 reverse names = 1.168.192.in-addr.arpa.

            ip4cidr/30 = 192.168.1.0/30
            ip4cidr/30 reverse names = 0.1.168.192.in-addr.arpa.
            ip4cidr/30 reverse names = 1.1.168.192.in-addr.arpa.
            ip4cidr/30 reverse names = 2.1.168.192.in-addr.arpa.
            ip4cidr/30 reverse names = 3.1.168.192.in-addr.arpa.

            ip6cidr/64 = fd93:59ef:8ce1:aac8::/64
            ip6cidr/64 reverse names = 8.c.a.a.1.e.c.8.f.e.9.5.3.9.d.f.ip6.arpa.

    """
    try:
        ip = IP( value )

        return ip.reverseNames()

    except ValueError:

        return ''

register.filter( 'reverse_names', reverse_names )


class rememberVarInContext(template.Node):

    def __init__(self, varname, varvalue ):

        self.varname = varname
        self.varvalue = varvalue

    def render(self, context):

        context[ self.varname ] = self.varvalue

        return ''


@register.tag(name='assign')
def do_assign(parser,token):

    """
        Variable assignment within template

        Usage: {% assign newvar = <space seperated list of strings/vars> %}
         i.e.: {% assign file_name = '/var/tmp/rack-' rack.label '.txt' %}
    """
    definition = token.split_contents()

    if len(definition) < 4:
        raise template.TemplateSyntaxError, '%r tag requires at least 4 arguments' % tag

    tag = definition[0]
    new_var = definition[1]
    is_teken = definition[2]
    assignees = definition[3:]

    return resolveVariables( new_var, assignees )

@register.assignment_tag
def to_list(*args):
    """
        Convert string to list

        Usage: 
		{% to_list 1 2 3 4 5 "yes" as my_list %}
		{% for i in my_list %}
		    {{ i }}
		{% endfor %}
    """
    return args

class resolveVariables(template.Node):

    def __init__(self, varname, varlist ):

        self.varname = varname
        self.varlist = varlist

    def render(self, context):
        resvars = [ ]

        for a in self.varlist:

            var_str = ''

            if not (a[0] == a[-1] and a[0] in ('"', "'")):
                try:
                    # RB: no quotes must mean its a variable
                    #
                    a_var = template.Variable( a )
                    var_str = a_var.resolve(context)

                except template.VariableDoesNotExist:

                    #RB: still think not allowed to raise exceptions from render function
                    #
                    #raise template.TemplateSyntaxError, 'cannot resolve variable %r' %(  str( self.path ) )
                    pass

                resvars.append( str(var_str) )

            else:
                #RB: assume strings are quoted
                #RB: strip quotes from string
                #
                a = str( a.strip("'").strip('"') )
                resvars.append( str(a) )

        #RB: finally assign the concatenated string to new varname
        context[ self.varname ] = string.join( resvars, '' )

        #RB: Django render functions not supposed/allowed to raise Exception, I think
        return ''

@register.tag(name='store')
def do_save_meta(parser, token):
    """
        Compilation function to use for meta-info.

        Usage: {% store '/path/to/file' %}
               {% store variable %} # variable = '/path/to/file'
    """
    definition = token.split_contents()

    if len(definition) != 4 and len(definition) != 2:
        raise template.TemplateSyntaxError, '%r tag requires at least 1 arguments' % tag

    tag = definition[0]
    path_arg = definition[1]

    if len(definition) == 4:

	    #RB: OLDSTYLE
        #RB: 4 arguments means: {% store /path/filename as output %}
        #RB: old style: DONT try to resolve variable
        #RB: instead convert filename to quoted string

        kw_as = definition[2]
        kw_output_name = definition[3]

        path_str = "'%s'" %path_arg

        # RB: parse the entire template for old-style
        nodelist = parser.parse()

    else:
    	#RB: NEWSTYLE
        #RB: 2 arguments can mean: {% store 'string' %}
        #RB: 2 arguments can mean: {% store variable %}

        kw_output_name = None

        path_str = path_arg

        # RB: parse the template thing until %endstore found
        nodelist = parser.parse(('endstore',))
        # RB: throw away %endstore tag
        parser.delete_first_token()

    # RB: Now lets start writing output files
    return generateStoreOutput(tag, path_str, nodelist, kw_output_name)

class generateStoreOutput(template.Node):

    def __init__(self, tag, path_str, nodelist, kw_output_name=None):
        self.tag = tag
        self.nodelist = nodelist
        self.path_str = path_str
        self.kw_output_name = kw_output_name

    def render(self, context):

        if (self.path_str[0] == self.path_str[-1] and self.path_str[0] in ('"', "'")):

            mypath_str = str(self.path_str)[1:-1]

        else:
            # RB: Not quoted: must be a variable: attempt to resolve to value
            try:
                pathvar = template.Variable( str(self.path_str) )
                mypath_str = pathvar.resolve(context)
            except template.VariableDoesNotExist:
                #raise template.TemplateSyntaxError, '%r tag argument 1: not a variable %r' %( tag, path_str )
                #TODO: handle this!
                pass

        if self.kw_output_name:
            # RB: store 'output' variable filename for BW compat

            context[ self.kw_output_name ] = mypath_str

        # RB: render template between store tags
        output = self.nodelist.render(context)

        # RB: store output in context dict for later writing to file
        if 'files' not in context['__template_outputfiles__']:
            context['__template_outputfiles__']['files'] = dict()
        context['__template_outputfiles__']['files'][mypath_str] = output

        if 'epilogue' not in context['__template_outputfiles__']:
            context['__template_outputfiles__']['epilogue'] = list()

        if context.has_key('epilogue') and context['epilogue']:
            for command in context['epilogue']:
                if command not in context['__template_outputfiles__']['epilogue']:
                    context['__template_outputfiles__']['epilogue'].append(command)

        # RB: output generated into context dict, so we return nothing
        return ''

class ScriptNode(template.Node):
    """
        Renderer, which executes the lines included in the script-tags.
    """

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        script = self.nodelist.render(context)

        script_lines = script.strip().splitlines()
        if context.has_key('epilogue'):
            context['epilogue'].extend(script_lines)
        else:
            context['epilogue'] = script_lines
        # All content between {% epilogue %} and {% endepilogue %} is parsed now
        return ''


@register.tag(name='epilogue')
def do_epilogue(parser, token):
    """
        Saving the contents between the epilogue-tags
    """
    nodelist = parser.parse(('endepilogue',))
    parser.delete_first_token()
    return ScriptNode(nodelist)


@register.tag(name='getbasenets')
def do_getbasenets(parser, token):

    try:
        tag, network_name, kw_as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires exactly 4 arguments' % tag

    return getBaseNets( varname, network_name )

class getBaseNets(template.Node):

    """
        Get list of basenets in a network (name)

        Usage: {% getbasenets <network name> as <listname> %}
    """

    def __init__(self, varname, network_name ):

        self.varname = varname
        self.network_name = network_name.strip("'").strip('"').__str__()
        self.basenets = [ ]

    def render(self, context):


        if (self.network_name[0] == self.network_name[-1] and self.network_name[0] in ('"', "'")):

            network_str = str( self.network_name.strip("'").strip('"') )
        else:
            # RB: Not quoted: must be a variable: attempt to resolve to value
            try:
                networkvar = template.Variable( str(self.network_name) )
                network_str = networkvar.resolve(context)
            except template.VariableDoesNotExist:
                #raise template.TemplateSyntaxError, '%r tag argument 1: not a variable %r' %( tag, path_str )
                pass

        from IPy import IP

        network_units = apps.get_model('cluster', 'Network').objects.filter( name=str(network_str) )

        for n in network_units:

            for ipnum in IP( n.cidr ):
                if not base_net( ipnum ) in self.basenets:
                    self.basenets.append( str( base_net( ipnum ) ) )

        context[ self.varname ] = self.basenets
        self.basenets = [ ]

        return ''

@register.tag(name='getracks')
def do_getracks(parser, token):

    try:
        tag, cluster, kw_as, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires exactly 4 arguments' % tag

    return getRacks( name, cluster )

class getRacks(template.Node):

    """
        Get list of racks in a cluster

        Usage: {% getracks <cluster> as <listname> %}
    """

    def __init__(self, name, cluster):

        self.name = name
        self.cluster = cluster.strip("'").strip('"').__str__()
        self.racks = [ ]

    def render(self, context):

        cluster_units = apps.get_model('cluster', 'Equipment').objects.filter( cluster__name=str(self.cluster) )

        for u in cluster_units:
            if u.rack not in self.racks:
                self.racks.append( u.rack )

        context[ self.name ] = self.racks
        return ''

@register.tag(name='read')
def do_read(parser, token):
    """
        Compilation function to definine Querysets for later use.
        
        Usage: {% read <entity> --get <attribute>=<value> [<attribute>=<value>..] as <list_name> %}
    """
    tag = token.contents.split()[0]

    try:
        definition = token.split_contents()
        # definition should look like ['read', <entity>, '--get', <query1>, <query2>, 'as', '<key>']
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires at least 6 arguments' % tag
    if len(definition) < 6:
        raise template.TemplateSyntaxError, '%r tag requires at least 6 arguments' % tag
    if definition[2] != '--get':
        raise template.TemplateSyntaxError, "second argument of %r tag has to be '--get'" % tag
    if definition[-2] != 'as':
        raise template.TemplateSyntaxError, "second to last argument of %r tag has to be 'as'" % tag

    entity = definition[1]
    query = definition[3:-2]
    key = definition[-1]

    return QuerySetNode(entity, query, key)

def remove_quotes( val ):

    return str( val.strip("'").strip('"') )

class QuerySetNode(template.Node):
    """
        Renderer, which fetches objects from the database.
    """

    def __init__(self, entity, query, key):
        self.entity = entity
        self.query = query
        self.key = key

    def render(self, context):

        filter_dict = { }
        myquery_str = ''

        for q in self.query:
            myquery_str = remove_quotes( q )

            if myquery_str.find( '=' ) == -1:
                # RB: No operator: must be a variable: attempt to resolve to value
                try:
                    queryvar = template.Variable( str(myquery_str) )
                    myquery_str = queryvar.resolve(context)
                except template.VariableDoesNotExist:
                    #raise template.TemplateSyntaxError, '%r tag argument 1: not a variable %r' %( tag, path_str )
                    pass

            if myquery_str.count( '=' ) > 1 and myquery_str.count( ',' ) > 0:
                myfilters_list = myquery_str.split( ',' )
            else:
                myfilters_list = [ myquery_str ]

            for myfilter in myfilters_list:

                attr, val = myfilter.split('=')

                val = remove_quotes( val )

                my_model = apps.get_model('cluster', self.entity)

                filter_dict[ str(attr) ] = str(val)

        # Get Model/Entity name, i.e.: Equipment
        model_name = apps.get_model('cluster', self.entity).__name__

        # Get ViewSet for this Model/Entity, i.e.: EquipmentViewSet
        e_viewset = eval( model_name + 'ViewSet' )

        # Get the filter class for this viewset, i.e.: EquipmentFilter
        v_filter = e_viewset.filter_class

        # Get the queryset for this viewset, i.e.: Equipment.objects.all()
        v_queryset = e_viewset.queryset

        # If we have queryset filters, apply those on the Model objects
        if len( filter_dict ) > 0:
            search_result = apps.get_model('cluster', self.entity).objects.filter(**filter_dict)
        # Or else we use the ViewSet's queryset
        else:
            search_result = v_queryset

        context[self.key] = search_result

        #logger.debug('context = %s'%context)

        return ''

# use <entity> with <attribute>=<value> as <key>
