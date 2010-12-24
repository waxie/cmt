from piston.handler import BaseHandler
from piston.utils import rc
from sara_cmt.cluster.models import Interface, WarrantyContract
from datetime import date, timedelta

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


class WarrantyHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT')
    model = WarrantyContract
    exclude = ('tags', 'note', 'created_on', 'type', ('tags', 'label'))

    def read(self, request, warranty_status=None):
        warranties = WarrantyContract.objects
        today = date.today()
        critical_period = timedelta(30)

        if warranty_status == 'expired':
            return warranties.filter(date_to__lt=str(today))
        elif warranty_status == 'active':
            return warranties.filter(date_from_lte=str(today),date_to_gte=str(today))
        elif warranty_status == 'critical':
            return warranties.filter(date_to__gte=str(today),date_to__lt=str(date.today()+critical_period))
        else:
            resp = rc.NOT_IMPLEMENTED
            return resp

    #def update(self, request, label, date_to, date_from):
    #    user = User.objects.get(username=username)
    #    if request.username != user:
    #        return rc.FORBIDDEN




