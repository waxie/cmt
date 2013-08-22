# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from sara_cmt.cluster.models import HardwareUnit, Cluster
from api.serializers import UserSerializer, GroupSerializer, HardwareSerializer, ClusterSerializer


from rest_framework.generics import(
    ListCreateAPIView
)


class HardwareAPIListCreateView(ListCreateAPIView):
    model = HardwareUnit
    queryset = HardwareUnit.objects.all()
    serializer_class = HardwareSerializer


class ClusterAPIListCreateView(ListCreateAPIView):
    model = Cluster
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    model = Group
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


#class HardwareViewSet(viewsets.ModelViewSet):
#    queryset = HardwareUnit.objects.all()
#    serializer_class = HardwareSerializer
#
#
#class ClusterViewSet(viewsets.ModelViewSet):
#    queryset = Cluster.objects.all()
#    serializer_class = ClusterSerializer


