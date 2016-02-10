from IPy import IP

import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def dns_arpanize(value):
    ip = IP(value)

    # Well the maker of IPy has his own way for arpanize which is not widely used
    #  <network>-<broadcast.<subnet> must be:
    #  <broadcast>-<network>.<subnet>
    reverse_name = ip.reverseName()

    # When it's a classless reverse do some extra magic
    if re.search(r'[0-9]+\-[0-9]+\.[0-9\.]+', reverse_name):
        parts = reverse_name.split('.')

        reverse_name = "-".join(parts[0].split('-')[::-1]) + "." + ".".join(parts[1:])
    # When there is a leading 0. remove it for a clean arpanize
    elif re.search(r'0\.[0-9\.]+', reverse_name):
        reverse_name = ".".join(reverse_name.split('.')[1:])

    # Remove the last dot
    return reverse_name.rstrip('.')