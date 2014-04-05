"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'cmt_server.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

class AllRecentActions(modules.DashboardModule):
    """
    Module that lists the recent actions for all users. Customized version of RecentActions, changed by Ramon Bastiaans.
    """
    
    title = _('Recent Actions')
    template = 'grappelli/dashboard/modules/all_recent_actions.html'
    limit = 10
    include_list = None
    exclude_list = None
    
    def __init__(self, title=None, limit=10, include_list=None,
                 exclude_list=None, **kwargs):
        self.include_list = include_list or []
        self.exclude_list = exclude_list or []
        kwargs.update({'limit': limit})
        super(AllRecentActions, self).__init__(title, **kwargs)
    
    def init_with_context(self, context):
        if self._initialized:
            return
        from django.db.models import Q
        from django.contrib.admin.models import LogEntry
        
        request = context['request']
        
        def get_qset(list):
            qset = None
            for contenttype in list:
                if isinstance(contenttype, ContentType):
                    current_qset = Q(content_type__id=contenttype.id)
                else:
                    try:
                        app_label, model = contenttype.split('.')
                    except:
                        raise ValueError('Invalid contenttype: "%s"' % contenttype)
                    current_qset = Q(
                        content_type__app_label=app_label,
                        content_type__model=model
                    )
                if qset is None:
                    qset = current_qset
                else:
                    qset = qset | current_qset
            return qset
            
        qs = LogEntry.objects.all()
            
        if self.include_list:
            qs = qs.filter(get_qset(self.include_list))
        if self.exclude_list:
            qs = qs.exclude(get_qset(self.exclude_list))
            
        self.children = qs.select_related('content_type', 'user')[:self.limit]
        self._initialized = True

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Group: Administration & Applications'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Applications'),
                    column=1,
                    css_classes=('collapse closed',),
                    exclude=('django.contrib.*',),
                ),
                modules.AppList(
                    _('Administration'),
                    column=1,
                    collapsible=True,
                    models=('django.contrib.*',),
                )
            ]
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=3,
            children=[
                {
                    'title': _('CMT Documentation'),
                    'url': 'https://oss.trac.surfsara.nl/',
                    'external': True,
                },
                {
                    'title': _('SURFsara Website'),
                    'url': 'https://www.surfsara.nl/',
                    'external': True,
                },
            ]
        ))
        
        # append a feed module
        self.children.append(modules.Feed(
            _('Latest CMT developments'),
            column=2,
            feed_url='https://oss.trac.surfsara.nl/cmt/timeline?ticket=on&milestone=on&changeset=on&repo-=on&repo-git=on&wiki=on&max=50&authors=&daysback=90&format=rss',
            limit=5
        ))
        self.children.append(modules.Feed(
            _('Latest SURFsara News'),
            column=2,
            feed_url='https://www.surfsara.nl/news/feed',
            limit=5
        ))
        
        # append a recent actions module
        self.children.append(AllRecentActions(
            _('All Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
        self.children.append(modules.RecentActions(
            _('My Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


