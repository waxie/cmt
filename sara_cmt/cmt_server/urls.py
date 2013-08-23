from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from django.core.urlresolvers import reverse
from sara_cmt.cluster.models import HardwareUnit, Cluster, Rack
from cmt_server.apps.api.serializers import UserSerializer, GroupSerializer, HardwareSerializer, ClusterSerializer, RackSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    model = Group
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class HardwareViewSet(viewsets.ModelViewSet):
    model = HardwareUnit
    queryset = HardwareUnit.objects.all()
    serializer_class = HardwareSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    model = Cluster
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class RackViewSet(viewsets.ModelViewSet):
    model = Rack
    queryset = Rack.objects.all()
    serializer_class = RackSerializer


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'hardware', HardwareViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'racks', RackViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    # Examples:
    # url(r'^$', 'cmt_server.views.home', name='home'),
    # url(r'^cmt_server/', include('cmt_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
