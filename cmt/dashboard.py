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

        # append the cmt client download link
        self.children.append(modules.LinkList(
            _('Downloads'),
            column=3,
            children=[
                {
                    'title': _('CMT Client'),
                    'url': reverse('download-cmt-client'),
                    'external': True,
                },
            ]
        ))
        
        # append a recent actions module
        self.children.append(AllRecentActions(
            _('All Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))
        self.children.append(modules.RecentActions(
            _('My Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))


