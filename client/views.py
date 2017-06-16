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

import cStringIO as StringIO
import os
import urlparse

from django.http.response import HttpResponse
from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required

from cmt.decorators import http_basic_auth

@http_basic_auth
@login_required
def download_client(request):
    file_path = os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        'cmt_client.py'
    )
    file_name = os.path.basename(file_path)

    new_file = StringIO.StringIO()

    CMT_INVENTORY = {}
    for model, model_cls in apps.get_app_config('cluster').models.items():
        if model in settings.CLIENT_SKIP_MODELS:
            continue

        if model not in CMT_INVENTORY:
            CMT_INVENTORY[model] = {
                'url': os.path.join('api', settings.CLIENT_API_VERSION, model),
                'fields': list()
            }
        for field in model_cls._meta.get_fields():
            CMT_INVENTORY[model]['fields'].append(field.name)
    CMT_INVENTORY['template'] = {
        'url': os.path.join('api', settings.CLIENT_API_VERSION, 'template'),
        'fields': list()
    }

    CMT_URL_PARTS = urlparse.ParseResult(
        scheme=request.scheme,
        netloc='%s:%s' % (request.META.get('SERVER_NAME', 'cmt.surfsara.nl'), request.META.get('SERVER_PORT', '443')),
        path='',
        params='',
        query='',
        fragment='',
    )

    with open(file_path, 'r') as fi:
        IN_CONFIG_MODE = False
        for line in fi:
            if line.strip() == '## START CONFIG':
                IN_CONFIG_MODE = True
                new_file.write('## START CONFIG\n')
                new_file.write('CMT_SERVER = \'%s\'\n' % urlparse.urlunparse(CMT_URL_PARTS))
                new_file.write('CMT_INVENTORY = %s\n' % str(CMT_INVENTORY))
                new_file.write('CMT_API_VERSION = \'%s\'\n' % str(settings.CLIENT_API_VERSION))
                new_file.write('CMT_TEMPLATEDIR = \'/etc/cmt/templates\'\n')
            elif line.strip() == '## END CONFIG':
                IN_CONFIG_MODE = False

            if IN_CONFIG_MODE:
                continue

            new_file.write(line)

    response = HttpResponse(
        content_type='text/x-python'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    response['Content-Length'] = new_file.tell()
    response.write(new_file.getvalue())

    return response
