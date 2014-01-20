### Create your views here.
##
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from django.db.models import Q

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


#class UserViewSet(viewsets.ModelViewSet):
#    """
#    Returns a list of **all** registered users.
#    
#    For more details about the user please [see here][ref].
#
#    [ref]: https://intranet.surfsara.nl/algemeen/wiki/Telefoonlijst
#    """
#    model = User
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

##class GroupViewSet(viewsets.ModelViewSet):
##    model = Group
##    queryset = Group.objects.all()
##    serializer_class = GroupSerializer
##
##class ClusterList(generics.ListAPIView):
##    queryset = Cluster.objects.all()
##    serializer_class = ClusterSerializer
##    lookup_field = 'pk'
##
##    def get_paginate_by(self):
##        """
##        Use smaller pagination for HTML representations.
##        """
##        if self.request.accepted_renderer.format == 'html':
##            return 2
##        return 20
##
##    def get_queryset(self):
##        return Cluster.objects.all()
##
##
#class ClusterList(generics.ListCreateAPIView):
#    queryset = Cluster.objects.all()
#    serializer_class = ClusterSerializer
#
#class ClusterDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Cluster.objects.all()
#    serializer_class = ClusterSerializer

#####
#
# Viewsets based on the models in CMT. They define the view behavior.
#

# Equipment-related
class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    filter_fields = ('name',)
    # model = Cluster
    # lookup_fields = (...

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_fields = ('cluster__name', 'rack__label')


## looks deprecated, since django-filter has been implemented now
#    def get_queryset(self):
#        #q = self.kwargs # (always?) empty dict
#        #print 'SELF.KWARGS', q, '(%s)'%type(q)
#        querydict = self.request.GET # dict (QueryDict) of kwargs
#        print 'SELF.REQUEST.get', querydict, '(%s)'%type(querydict)
#        #print 'self.request.query_params', self.request.QUERY_PARAMS
#
#        d = {}
#        for key, val in querydict.iterlists():
#            #print "KEY %s (%s) VAL %s (%s)"%(key, type(key), val, type(val))
#            if isinstance(val, list):
#                d['%s__in'%key] = val
#            else:
#                d[key] = val
#        for key, val in querydict.iterlists():
#            d['%s__in'%key] = val
#
#        queryset = Equipment.objects.filter(**d)
#        print 'QSET', queryset
#        return queryset
#
#
#    def list(self, request):
#        querydict = self.request.GET # dict (QueryDict) of kwargs
#        #print 'SELF.REQUEST.get', querydict, '(%s)'%type(querydict)
#        #print 'self.request.query_params', self.request.QUERY_PARAMS
#        query = None
#        for key, val in querydict.iterlists():
#            #print "KEY %s VAL %s"%(key,val)
#            if query is None:
#                #print 'QUERY is NONE'
#                if isinstance(val, list):
#                    #print 'VAL is LIST'
#                    query = Q(**{'%s__in'%key: val})
#                else:
#                    #print 'VAL is not LIST'
#                    query = Q(**{key: val})
#            else:
#                #print 'QUERY is not NONE'
#                if isinstance(val, list):
#                    query &= Q(**{'%s__in'%key: val})
#                else:
#                    #print 'VAL is not LIST'
#                    query &= Q(**{'%s__in'%key: val})
#        #print "QUERY", query
#        queryset = Equipment.objects.filter(query)
#        #print 'QSET', queryset
#
#        serializer = EquipmentSerializer(queryset, many=True)
#        #print 'SERIALIZER', serializer
#        return Response(serializer.data)
##

class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    filter_fields = ('label', )

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# Network-related
class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer

class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class TelephonenumberViewSet(viewsets.ModelViewSet):
    queryset = Telephonenumber.objects.all()
    serializer_class = TelephonenumberSerializer


class HardwareModelViewSet(viewsets.ModelViewSet):
    queryset = HardwareModel.objects.all()
    serializer_class = HardwareModelSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class InterfaceTypeViewSet(viewsets.ModelViewSet):
    queryset = InterfaceType.objects.all()
    serializer_class = InterfaceTypeSerializer


class WarrantyTypeViewSet(viewsets.ModelViewSet):
    queryset = WarrantyType.objects.all()
    serializer_class = WarrantyTypeSerializer


class WarrantyContractViewSet(viewsets.ModelViewSet):
    queryset = WarrantyContract.objects.all()
    serializer_class = WarrantyContractSerializer
