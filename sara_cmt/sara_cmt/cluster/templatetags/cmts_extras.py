from django import template

register = template.Library()


@register.filter
def cut(value, arg):
  return value.replace(arg, '')
cut.is_safe = True
