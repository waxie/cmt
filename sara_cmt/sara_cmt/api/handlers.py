from piston.handler import BaseHandler
from sara_cmt.cluster.models import Interface

# Some notes:
#
# read() is called on GET requests:
#   Should never modify data (idempotent).
# create() is called on POST requests:
#   Creates new objects, and should return them (or rc.CREATED).
# update() is called on PUT requests:
#   Should update an existing product and return them (or rc.ALL_OK).
# delete() is called on DELETE requests:
#   Should delete an existing object, and not return anything, just rc.DELETED.

class InterfaceHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Interface
    #fields = ('network', 'host')
    #exclude = ('created_on', 'updated_on')

    def read(self, request, interface_label=None):
        base = Interface.objects
        if interface_label:
            return base.get(label=interface_label)
        else:
            return base.all() # Or base.filter(...)
    
