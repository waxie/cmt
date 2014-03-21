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

import os, re, string

# Inspired by Django tips on:
#   http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_unicode, force_unicode

from sara_cmt.logger import Logger
logger = Logger().getLogger()

#from django.db.models import get_model

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

@stringfilter
def arpanize(value):
    """
        Converts a IP (range) to reversed DNS style arpa notation

        Usage:
            {{{ <variable>|arpanize }}}

        I.e.:
            {% assign broadcast = '192.168.1.0' %}
            {{{ broastcast|arpanize }}}
        Results in output:
            1.168.192.in-addr.arpa
    """
    ip_blocks = value.split('.')

    reverse_block = [ ip_blocks[2], ip_blocks[1], ip_blocks[0], 'in-addr.arpa' ]

    return string.join( reverse_block, '.' )

register.filter( 'arpanize', arpanize )

@stringfilter
def base_net(value):
    """
        Converts a IP (range) to it's first 3 octects

        Usage:
            {{{ <variable>|base_net }}}

        I.e.:
            {% assign broadcast = '192.168.1.0' %}
            {{{ broastcast|base_net }}}
        Results in output:
            192.168.1
    """
    ip_blocks = value.split('.')

    return string.join( ip_blocks[:3], '.' )

register.filter( 'base_net', base_net )

@stringfilter
def ip_last_digit(value):
    """
        Converts a IP (range) to it's last octect

        Usage:
            {{{ <variable>|ip_last_digit }}}

        I.e.:
            {% assign myip = '192.168.1.123' %}
            {{{ myip|ip_last_digit }}}
        Results in output:
            123
    """
    ip_blocks = value.split('.')

    return ip_blocks[3]

register.filter( 'ip_last_digit', ip_last_digit )

@register.tag(name='diff_ignore')
def do_diff_ignore(parser,token):
    """
        RegExp of lines to ignore in diff checking original/new output files

        Usage: {% diff_ignore <space seperated list of regexps> %}
         i.e.: {% diff_ignore '^#.*$' '^$' %}
               to ignore lines starting with #, and empty lines 

        This setting can differ for different output files, if it is used within store tags.
        If it is set outside store tags, it is a global setting for all output files in this template

        Since diff checking is (optionally) done by the client, the list is simply returned by the API in JSON
    """
    definition = token.split_contents()

    if len(definition) < 2:
        raise template.TemplateSyntaxError, '%r tag requires at least 2 arguments' % tag

    tag = definition[0]
    ignore_regexps = definition[1:]

    clean_ignore_regexps = [ ]

    for r in ignore_regexps:

        clean_ignore_regexps.append( r.strip("'").strip('"') )

    return rememberVarInContext( '$cmt$diff_ignore', clean_ignore_regexps )

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
                pass

        if self.kw_output_name:
            # RB: store 'output' variable filename for BW compat

            context[ self.kw_output_name ] = mypath_str

        # RB: render template between store tags
        output = self.nodelist.render(context)

        # RB: store output in context dict for later writing to file
        context['__template_outputfiles__'][ mypath_str ] = { }
        context['__template_outputfiles__'][ mypath_str ][ 'contents' ] = output

        if context.has_key( '$cmt$diff_ignore' ):
            context['__template_outputfiles__'][ mypath_str ][ 'diff_ignore' ] = context['$cmt$diff_ignore']
        else:
            context['__template_outputfiles__'][ mypath_str ][ 'diff_ignore' ] = ''

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
        if context.has_key('epilogue'):
            context['epilogue'].append(script)
        else:
            context['epilogue'] = [script]
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

from django.db.models import get_model

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

        network_units = get_model('cluster', 'Network').objects.filter( name=str(network_str) )

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

        cluster_units = get_model('cluster', 'HardwareUnit').objects.filter( cluster__name=str(self.cluster) )

        for u in cluster_units:
            if u.rack not in self.racks:
                self.racks.append( u.rack )

        context[ self.name ] = self.racks
        return ''

@register.tag(name='use')
def do_use(parser, token):
    """
        Compilation function to definine Querysets for later use.
        
        Usage: {% use <entity> with <attribute>=<value> as <list/var> <key> %}
    """
    tag = token.contents.split()[0]

    try:
        definition = token.split_contents()
        # definition should look like ['use', <entity>, 'with' <query>, 'as', '<key>']
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires at least 5 arguments' % tag
    if len(definition) != 6:
        raise template.TemplateSyntaxError, '%r tag requires at least 5 arguments' % tag
    if definition[2] != 'with':
        raise template.TemplateSyntaxError, "second argument of %r tag has to be 'with'" % tag
    if definition[-2] != 'as':
        raise template.TemplateSyntaxError, "second last argument of %r tag has to be 'as'" % tag

    entity = definition[1]
    query = definition[-3]
    key = definition[-1]

    return QuerySetNode(entity, query, key)

class QuerySetNode(template.Node):
    """
        Renderer, which fetches objects from the database.
    """

    def __init__(self, entity, query, key):
        self.entity = entity
        self.query = query
        self.key = key

    def render(self, context):

        if (self.query[0] == self.query[-1] and self.query[0] in ('"', "'")):

            myquery_str = str( self.query.strip("'").strip('"') )
        else:
            # RB: Not quoted: must be a variable: attempt to resolve to value
            try:
                queryvar = template.Variable( str(self.query) )
                myquery_str = queryvar.resolve(context)
            except template.VariableDoesNotExist:
                #raise template.TemplateSyntaxError, '%r tag argument 1: not a variable %r' %( tag, path_str )
                pass

        if myquery_str.count( '=' ) > 1 and myquery_str.count( ',' ) > 0:

            myfilters_list = myquery_str.split( ',' )
        else:
            myfilters_list = [ myquery_str ]

        filter_dict = { }

        for myfilter in myfilters_list:

            attr, val = myfilter.split('=')
            filter_dict[ attr ] = val

        queryset = get_model('cluster', self.entity).objects.filter(**filter_dict)
        if len(queryset) == 1:
            queryset = queryset[0]
        context[self.key] = queryset
        #logger.debug('context = %s'%context)
        return ''

# use <entity> with <attribute>=<value> as <key>
