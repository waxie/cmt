from django.conf.urls.defaults import *
from django.contrib import databrowse

#from sara_cmt import cluster

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^core/', include('core.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^db/(.*)', databrowse.site.root),
)

from cluster.models import *
databrowse.site.register(Cluster)
databrowse.site.register(Site)
databrowse.site.register(Contact)
databrowse.site.register(Rack)
databrowse.site.register(Interface)
databrowse.site.register(InterfaceType)
databrowse.site.register(HardwareUnit)
databrowse.site.register(Role)
databrowse.site.register(Network)
databrowse.site.register(HardwareSpecifications)
databrowse.site.register(Company)
databrowse.site.register(Position)
databrowse.site.register(Department)
databrowse.site.register(Warranty)
from tagging.models import *
databrowse.site.register(Tag)
databrowse.site.register(TaggedItem)
