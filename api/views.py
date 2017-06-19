#
# This file is part of CMT
#
# CMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# CMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMT.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2017 SURFsara

from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import CHANGE
from django.core.exceptions import FieldError
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType
from django.template import Context
from django.template import TemplateSyntaxError
from django.http import JsonResponse
from django.template import loader

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser

from api.serializers import *
from api.filters import *

from cluster.models import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2000
    page_size_query_param = 'page_size'
    max_page_size = 5000


def django_admin_logentry(action, object, user):

    actions = {
        'create': ADDITION,
        'update': CHANGE,
        'delete': DELETION
    }

    # For now when we don't now it, just ignore it
    if action not in actions:
        return False

    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_unicode(object),
        action_flag=actions[action],
        change_message='API'
    )

    return True

class CMTViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        object = serializer.save()
        django_admin_logentry('create', object, self.request.user)

    def perform_update(self, serializer):
        object = serializer.save()
        django_admin_logentry('update', object, self.request.user)

    def perform_destroy(self, instance):
        django_admin_logentry('delete', instance, self.request.user)
        instance.delete()

    def get_serializer_context(self):
       """
       Extra context provided to the serializer class.
       RB: pass extra "fields" args along, which optionally specifies which fields to return
       """
       fields = self.request.query_params.get('fields', None)

       return {
           'request': self.request,
           'format': self.format_kwarg,
           'view': self,
           'fields': fields
       }

    def get_queryset(self):
        """
        Optionally filters the returned queryset based on query arguments
        This allows things like this to work: label__startswith=r7
        """

        queryset = self.serializer_class.Meta.model.objects.all()
        q_filter_dict = { }
        for attr, val in self.request.query_params.items():
            if not attr or not val:
                continue

            # only do this for queryset filters that contain __ (i.e.: label__startswith)
            # all other filters should (and will) be handled by filter_class (django-filter)
            if str(attr).find( '__' ) != -1:
                q_filter_dict[ str(attr) ] = str(val)

        # Perform that queryset filtering magic
        if len(q_filter_dict) > 0:
            try:
                queryset = queryset.filter( **q_filter_dict )
            except FieldError as details:
                # someone is making a typo: but we can't return an error to client from here
                # So they should learn to type and simply return to original queryset
                queryset = queryset
        else:
            queryset = queryset

        return queryset


class ClusterViewSet(CMTViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    filter_class = ClusterFilter


class EquipmentViewSet(CMTViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_class = EquipmentFilter


class RackViewSet(CMTViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    filter_class = RackFilter


class RoomViewSet(CMTViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_class = RoomFilter


class AddressViewSet(CMTViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_class = AddressFilter


class CountryViewSet(CMTViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_class = CountryFilter


class RoleViewSet(CMTViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_class = RoleFilter


class ConnectionViewSet(CMTViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filter_class = ConnectionFilter


class CompanyViewSet(CMTViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_class = CompanyFilter


class HardwareModelViewSet(CMTViewSet):
    queryset = HardwareModel.objects.all()
    serializer_class = HardwareModelSerializer
    filter_class = HardwareModelFilter


class NetworkViewSet(CMTViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_class = NetworkFilter


class WarrantyContractViewSet(CMTViewSet):
    queryset = WarrantyContract.objects.all()
    serializer_class = WarrantyContractSerializer
    filter_class = WarrantyContractFilter


class InterfaceViewSet(CMTViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    filter_class = InterfaceFilter


class InterfaceTypeViewSet(CMTViewSet):
    queryset = InterfaceType.objects.all()
    serializer_class = InterfaceTypeSerializer
    filter_class = InterfaceTypeFilter


class WarrantyTypeViewSet(CMTViewSet):
    queryset = WarrantyType.objects.all()
    serializer_class = WarrantyTypeSerializer
    filter_class = WarrantyTypeFilter


class TelephonenumberViewSet(CMTViewSet):
    queryset = Telephonenumber.objects.all()
    serializer_class = TelephonenumberSerializer
    filter_class = TelephonenumberFilter


class TemplateView(APIView):

    parser_classes = (FileUploadParser,)
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        file_obj = request.data['file']

        try:
            template_data = {
                'version': '2.1.0',
                'svn_id': '$Id',
                'input': file_obj.temporary_file_path(),
                '__template_outputfiles__': {},
                'epilogue': list()
            }
            context = Context(template_data)

            try:
                tpl = loader.get_template(file_obj.temporary_file_path())
                tpl.render(template_data)
            except TemplateSyntaxError as error:
                return JsonResponse({'error': str(error)})
        except IOError as error:
            return JsonResponse({'status': 500})

        file_obj.close()

        return JsonResponse(context['__template_outputfiles__'])
