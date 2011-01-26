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


class MetaNode(template.Node):
    """
        Renderer, which stores the save path to the context.
    """

    def __init__(self, tag, values):
        self.tag = tag
        self.values = values

    def render(self, context):
        # This is where the work actually happens
        context[self.tag] = self.values
        return ''


@stringfilter
def base_net(value):
    ip_blocks = value.split('.')

    return string.join( ip_blocks[:3], '.' )

register.filter( 'base_net', base_net )

@stringfilter
def ip_last_digit(value):
    ip_blocks = value.split('.')

    return ip_blocks[3]

register.filter( 'ip_last_digit', ip_last_digit )

@register.tag(name='store')
def do_save_meta(parser, token):
    """
        Compilation function to use for meta-info.

        Usage: {% store '/path/to/file' %}
               {% store variable %} # variable = '/path/to/file'
    """
    try:
        # RB: split_contents respects quoted 'strings containing spaces'
        tag, path_str = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires at least 1 argument' % tag

    path = None

    if not (path_str[0] == path_str[-1] and path_str[0] in ('"', "'")):
        # RB: Not quoted: must be an variable: attempt to resolve to value
        try:
            path = template.Variable( path_str )
        except template.VariableDoesNotExist:
            raise template.TemplateSyntaxError, '%r tag argument 1: not an variable %r' %( tag, path_str )
        else:
            path_str = ''
    else:
        # RB: remove the quotes
        path_str = path_str[1:-1]

    # RB: parse the template thing until %endstore found
    nodelist = parser.parse(('endstore',))
    parser.delete_first_token()

    # RB: Now lets start writing output files
    return generateStoreOutput(tag, path, path_str, nodelist)

class generateStoreOutput(template.Node):

    def __init__(self, tag, path, path_str, nodelist):
        self.tag = tag
        self.nodelist = nodelist
        self.path = path
        self.path_str = path_str

    def render(self, context):
        if self.path_str == '':
            try:
                self.path_str = self.path.resolve(context)
            except template.VariableDoesNotExist:
                raise template.TemplateSyntaxError, '%r tag argument 1: cannot resolve variable %r' %( self.tag, str( self.path ) )

	# RB: render template between store tags
        output = self.nodelist.render(context)

	if not context.has_key( 'stores' ):
		context['stores'] = {}

	# RB: store output in context dict for later writing to file
        context['stores'][ self.path_str ] = output

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
    #attr,val = query.split('=')
    key = definition[-1]
    #queryset = get_model('cluster', entity).objects.filter(**{attr:val})
    #return ObjectNode(definition[-1], definition[1])
    return QuerySetNode(entity, query, key)


class QuerySetNode(template.Node):
    """
        Renderer, which fetches objects from the database.
    """

    def __init__(self, entity, query, key):
        self.entity = entity
        self.query = query.strip("'").strip('"').__str__()
        self.key = key

    def render(self, context):
        attr, val = self.query.split('=')
        queryset = get_model('cluster', self.entity).objects.filter(**{attr:val})
        if len(queryset) == 1:
            queryset = queryset[0]
        context[self.key] = queryset
        logger.debug('context = %s'%context)
        return ''


# use <entity> with <attribute>=<value> as <key>


        
