from piston.handler import BaseHandler
from sara_cmt.cluster.models import Interface

class InterfaceHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Interface

    def read(self, request, interface_label=None):
        base = Interface.objects
        if interface_label:
            return base.get(label=interface_label)
        else:
            return base.all() # Or base.filter(...)
    
