from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.models import User, Group
from rest_framework import routers
#from django.core.urlresolvers import reverse
from cmt_server.apps.api.views import *
##from cmt_server.apps.api.serializers import UserSerializer, GroupSerializer
##
##from cmt_server.apps.api.views import ClusterList
##
##
##class MultipleFieldLookupMixin(object):
##    """
##    Apply this mixin to any view or viewset to get multiple field filtering
##    based on a 'lookup_fields' attribute, instead of default single field filtering.
##    """
##    def get_paginate_by(self):
##        """
##        Use smaller pagination for HTML representations.
##        """
##        if self.request.accepted_renderer.format == 'html':
##            return 20
##        print 'TEST'
##        return 2
##
##    def get_queryset(self):
##        print 'GET_QUERYSET'
##        print self.kwargs
##        #queryset = self.model.objects.all()
##        #filter = {}
##        #for field in self.kwargs.keys():
##        #    filter[field] = self.kwargs[field]
##        ##obj = get_queryset_or_404(queryset, **filter) # Lookup the object
##        #print 'FILTER:', filter
##        #obj = queryset.filter(**filter) # Lookup the object
##        #return obj
##
##    def get_object(self):
##        queryset = self.get_queryset() # Get the base queryset
##        queryset = self.filter_queryset(queryset) # Apply any filter backends
##        filter = {}
##        for field in self.multiple_lookup_fields:
##            filter[field] = self.kwargs[field]
##        obj = get_object_or_404(queryset, **filter) # Lookup the object
##        return obj
##
##
##
##
##
##
# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
##router.register(r'users', UserViewSet)
##router.register(r'groups', GroupViewSet)

## locations of equipment in a cluster
router.register(r'clusters', ClusterViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'racks', RackViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'countries', CountryViewSet) # not really necessary
router.register(r'rooms', RoomViewSet)

## network-related info of equipment
router.register(r'interfaces', InterfaceViewSet)
router.register(r'networks', NetworkViewSet)

## contact-related info of relations
router.register(r'contacts', ConnectionViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'telephonenumbers', TelephonenumberViewSet)

## equipment-related info
router.register(r'hardwaremodels', HardwareModelViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'interfacetypes', InterfaceTypeViewSet)

## warranty-related info
router.register(r'warrantytypes', WarrantyTypeViewSet)
router.register(r'warrantycontracts', WarrantyContractViewSet)

#from rest_framework import renderers
#
#cluster_list = ClusterViewSet.as_view({
#    'get': 'list',
#    'post': 'create'
#})
#cluster_detail = ClusterViewSet.as_view({
#    'get': 'retrieve',
#    'put': 'update',
#    #'patch': 'partial_upgrade',
#    'delete': 'destroy'
#})



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Examples:
    # url(r'^$', 'cmt_server.views.home', name='home'),
    # url(r'^cmt_server/', include('cmt_server.foo.urls')),

    #url(r'^clusters/', ListAPIView.as_view(model=Cluster), name='cluster-list'),
    #url(r'^clusters/(.+)$', ClusterViewSet.as_view()),
    #url(r'^clusters/$', cluster_list, name='cluster-list'),
    #url(r'^clusters/(?P<pk>[0-9]+)/$', cluster_detail, name='cluster-detail'),
    #url(r'^clusters/$',
    #    ClusterList.as_view()),
    #url(r'^clusters/(?P<pk>[0-9]+)/$',
    #    ClusterDetail.as_view(),
    #    name='cluster-detail'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
