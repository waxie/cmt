#    This file is part of CMT, a Cluster Management Tool made at SURFsara.
#    Copyright (C) 2012, 2013  Sil Westerveld, Ramon Bastiaans
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#
# Add this to apache config:
#
#  WSGIDaemonProcess cmt user=www-data group=www-data threads=25
#  WSGIProcessGroup cmt
#
#  WSGIPassAuthorization On
#
#  SetEnv VIRTUALENV /path/to/virtualenvs/cmt
#  WSGIScriptAlias / /path/to/virtualenvs/cmt/wsgi/cmt.wsgi
#
#  Alias /static  /path/to/virtualenvs/cmt/lib/python<ver>/site-packages/cmt_server/static
#

import os

from exceptions import SystemExit

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmt_server.settings")

def application(environ, start_response):
    ## Try to activate a virtualenv environment when the
    ## VIRTUALENV environ var is set
    virtualenv = environ.get('VIRTUALENV', False)

    if virtualenv and os.path.exists(virtualenv):
        activate_this = os.path.join(virtualenv, 'bin/activate_this.py')
        if os.path.exists(activate_this):
            execfile(activate_this, dict(__file__=activate_this))

    err_msgs = None

    try:
        from django.core.wsgi import get_wsgi_application
        from django.core.exceptions import ImproperlyConfigured

        return get_wsgi_application()(environ, start_response)

    except SystemExit as details:

        err_msgs = str( details )

    except ImportError as details:

        err_msgs = str( details )

    except ImproperlyConfigured as details:

        err_msgs = str( details )

    if err_msgs:

        start_response('200 OK',[('Content-type','text/html')])
        return ['<html><body><h1>Unable to load CMT/Django environment!</h1><p>' + err_msgs + '</p></body></html>']
