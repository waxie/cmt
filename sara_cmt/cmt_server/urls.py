from django.conf.urls.defaults import patterns, include, url

from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from apps.api.resources import ClusterResource, ContractResource, EquipmentResource, NetworkResource

from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.response import Response

from django.core.urlresolvers import reverse

class ExampleView(ResponseMixin, View):
    renderers = DEFAULT_RENDERERS

    def get(self, request):
        response = Response(200, {'description': 'Some example content', 'url': reverse('mixin-view')})
        return self.render(response)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cmt_server.views.home', name='home'),
    # url(r'^cmt_server/', include('cmt_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Django REST framework:
    (r'^api/cluster/$', ListOrCreateModelView.as_view(resource=ClusterResource)),
    (r'^api/cluster/(?P<name>[A-Za-z0-9]+)/$', InstanceModelView.as_view(resource=ClusterResource)),
    (r'^api/contract/$', ListOrCreateModelView.as_view(resource=ContractResource)),
    (r'^api/contract/(?P<label>[A-Za-z0-9]+)/$', InstanceModelView.as_view(resource=ContractResource)),
    (r'^api/equipment/$', ListOrCreateModelView.as_view(resource=EquipmentResource)),
    (r'^api/equipment/(?P<label>[A-Za-z0-9]+)/$', InstanceModelView.as_view(resource=EquipmentResource)),
    (r'^api/network/$', ListOrCreateModelView.as_view(resource=NetworkResource)),
    (r'^api/network/(?P<name>[A-Za-z0-9]+)/$', InstanceModelView.as_view(resource=NetworkResource)),
    url(r'^$', ExampleView.as_view(), name='mixin-view'),
)
