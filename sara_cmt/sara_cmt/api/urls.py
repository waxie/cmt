from django.conf.urls.defaults import *
from piston.resource import Resource
from sara_cmt.api.handlers import InterfaceHandler, WarrantyHandler

interface_handler = Resource(InterfaceHandler)
warranty_handler = Resource(WarrantyHandler)

urlpatterns = patterns('',
    #url(<url>, <resource>, [<emitter_format>]),
    url(r'interface/(?P<interface_label>[^/]+)/', interface_handler),
    url(r'interfaces/', interface_handler),
    url(r'warranties/(?P<warranty_status>[^/]*)', warranty_handler),
)
