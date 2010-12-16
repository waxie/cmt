from django.conf.urls.defaults import *
from piston.resource import Resource
from sara_cmt.api.handlers import InterfaceHandler

interface_handler = Resource(InterfaceHandler)

urlpatterns = patterns('',
    url(r'interface/(?P<interface_label>[^/]+)/', interface_handler),
    url(r'interfaces/', interface_handler),
)
