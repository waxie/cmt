import os

# Inspired by Django tips on:
#   http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/
from django import template
from django.template.defaultfilters import stringfilter

from sara_cmt.logger import Logger
logger = Logger().getLogger()

#from django.db.models import get_model

register = template.Library()

class MetaNode(template.Node):
  """
    Renderer, which stores the save path to the context.
  """
  def __init__(self, tag, vars):
    self.tag = tag
    self.vars = vars

  def render(self, context):
    # This is where the work actually happens
    context[self.tag] = self.vars
    return ''


@register.tag(name='store')
#@stringfilter
def do_save_meta(parser, token):
  """
    Compilation function to use for meta-info.
  """
  tag = token.contents.split()[0]
  try:
    meta_info = token.split_contents()
    # meta_info should look like ['<tag>', '<path>', 'as', '
  except ValueError:
    raise template.TemplateSyntaxError, '%r tag requires at least 3 arguments' % tag
  if len(meta_info) != 4:
    raise template.TemplateSyntaxError, '%r tag requires at least 3 arguments' % tag
  if meta_info[-2] != 'as':
    raise template.TemplateSyntaxError, "second last argument of %r tag has to be 'as'" % tag
  return MetaNode(meta_info[-1], meta_info[1])


class ScriptNode(template.Node):
  """
    Renderer, which executes the lines included in the script-tags.
  """
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    script = self.nodelist.render(context)
    context['epilogue'] = script
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
