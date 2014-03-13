# vim: set noai tabstop=4 shiftwidth=4 expandtab:

import pprint

### Create your views here.
##
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from sara_cmt.cluster.models import Cluster, Rack, Room, Address, Country
from sara_cmt.cluster.models import HardwareUnit as Equipment
from sara_cmt.cluster.models import Interface, Network
from sara_cmt.cluster.models import Connection, Company, Telephonenumber
from sara_cmt.cluster.models import HardwareModel, Role, InterfaceType
from sara_cmt.cluster.models import WarrantyType, WarrantyContract

from cmt_server.apps.api.serializers import ClusterSerializer, EquipmentSerializer, RackSerializer, RoomSerializer, AddressSerializer, CountrySerializer
from cmt_server.apps.api.serializers import InterfaceSerializer, NetworkSerializer
from cmt_server.apps.api.serializers import ConnectionSerializer, CompanySerializer, TelephonenumberSerializer
from cmt_server.apps.api.serializers import HardwareModelSerializer, RoleSerializer, InterfaceTypeSerializer
from cmt_server.apps.api.serializers import WarrantyTypeSerializer, WarrantyContractSerializer

from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType


from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView


#class CMTViewSet(ListBulkCreateUpdateDestroyAPIView):
class CMTViewSet(viewsets.ModelViewSet):

    def pre_delete(self, obj):

        """
        pre_delete hook is called by ModelViewSet before deleting a object from database

        Log entry to django-admin log
        """

        LogEntry.objects.log_action(
            user_id         = self.request.user.pk, 
            content_type_id = ContentType.objects.get_for_model(obj).pk,
            object_id       = obj.pk,
            object_repr     = force_unicode(obj), 
            action_flag     = DELETION
        )

    def post_save(self, obj, created=False):

        """
        post_save hook is called by ModelViewSet after saving a object to database

        created indicates if the object was changed (existing) or added (new)

        Log entry to django-admin log
        """

        if created:

            LogEntry.objects.log_action(
                user_id         = self.request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(obj).pk,
                object_id       = obj.pk,
                object_repr     = force_unicode(obj), 
                action_flag     = ADDITION
            )

        else:

            LogEntry.objects.log_action(
                user_id         = self.request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(obj).pk,
                object_id       = obj.pk,
                object_repr     = force_unicode(obj), 
                action_flag     = CHANGE
            )

#####
#
# Viewsets based on the models in CMT. They define the view behavior.
# Documented at: http://www.django-rest-framework.org/
#

# Equipment-related
class ClusterViewSet(CMTViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    fields = ('url', 'name')
    filter_fields = ('name',)
    #search_fields = ('name',)
    # model = Cluster
    # lookup_fields = (...

class EquipmentViewSet(CMTViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_fields = (
            'cluster__name', 'role__label', 'network__name', 'network__vlan',
            'specifications__name', 'warranty__label', 'warranty__contract_number',
            'rack__label', 'warranty_tag', 'serial_number', 'first_slot', 'label',
            #'in_support'
            )
    #search_fields = (
    #        'cluster__name', 'rack__label'
    #        )


class RackViewSet(CMTViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    filter_fields = ('label', 'room__label')

class RoomViewSet(CMTViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('label', 'address__address')

class AddressViewSet(CMTViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_fields = ( 'address',
            'postalcode', 'city', 'country__name', 'country__country_code'
            )



class CountryViewSet(CMTViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_fields = ('name', 'country_code')


# Network-related
class InterfaceViewSet(CMTViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    filter_fields = (
            'network__name', 'network__vlan', 'host__label', 'iftype__label',
            'label', 'aliases', 'hwaddress', 'ip'
            )

class NetworkViewSet(CMTViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_fields = (
            'name', 'cidr', 'gateway', 'domain', 'vlan'
            )


class ConnectionViewSet(CMTViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filter_fields = ('name',)


class CompanyViewSet(CMTViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_fields = ('name',)


class TelephonenumberViewSet(CMTViewSet):
    queryset = Telephonenumber.objects.all()
    serializer_class = TelephonenumberSerializer
    filter_fields = ('connection__name',)


class HardwareModelViewSet(CMTViewSet):
    queryset = HardwareModel.objects.all()
    serializer_class = HardwareModelSerializer
    filter_fields = ('vendor__name', 'name', 'vendorcode')


class RoleViewSet(CMTViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_fields = ('label',)


class InterfaceTypeViewSet(CMTViewSet):
    queryset = InterfaceType.objects.all()
    serializer_class = InterfaceTypeSerializer
    filter_fields = ('vendor__name', 'label')


class WarrantyTypeViewSet(CMTViewSet):
    queryset = WarrantyType.objects.all()
    serializer_class = WarrantyTypeSerializer
    filter_fields = ('contact__name', 'label')


class WarrantyContractViewSet(CMTViewSet):
    queryset = WarrantyContract.objects.all()
    serializer_class = WarrantyContractSerializer
    filter_fields = ('warranty_type__label', 'contract_number', 'label')

class TemplateView(APIView):
    parser_classes = (FileUploadParser,)
    authentication_classes = (authentication.BasicAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):

        file_obj  = request.FILES['file']
        file_name = file_obj.name

        file_fullpath = file_obj.temporary_file_path()

        #print file_fullpath

        #return Response(status=204)

        #pprint.pprint( request )
        #print file_obj.readlines()

        from django.template import Context
        from django.template.loader import render_to_string
        from django.template import TemplateDoesNotExist
        from django.http import HttpResponse
        import json

        try:
            # Initialize a Context to render the template with
            template_data = {}
            template_data['version'] = '2.0+GIT'
            template_data['svn_id'] = '$Id:$'
            template_data['svn_url'] = '$URL:$'
            template_data['input'] = file_fullpath
            template_data['__template_outputfiles__'] = {} # reserved for data to write to files
            template_data['epilogue'] = []
            context = Context(template_data)

            template_data['stores'] = template_data['__template_outputfiles__'] # to stay bw compatible with ramon's code (temporary)

            rendered_string = render_to_string(file_fullpath, context_instance=context)
            # While rendering the template there are variables added to the
            # Context, so these can be used for post-processing.
            #logger.debug('<RESULT>\n%s\n</RESULT>'%rendered_string)

        except IOError, e:
            return Response(status=500)
            #logger.error('Template does not exist: %s' % e)

        #pprint.pprint( context['__template_outputfiles__'] )

        file_obj.close()

        return HttpResponse(json.dumps(context['__template_outputfiles__']), content_type="application/json")
