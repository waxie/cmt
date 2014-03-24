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
#  WSGIScriptAlias / /path/to/virtualenvs/cmt/cmt.wsgi
#  SetEnv VIRTUALENV /path/to/virtualenvs/cmt
#
#  Alias /static /path/to/virtualenvs/cmt/lib/python<ver>/site-packages/sara_cmt/static
#

import os
import sys
import re

def application(environ, start_response):
    ## Try to activate a virtualenv environment when the
    ## VIRTUALENV environ var is set
    virtualenv = environ.get('VIRTUALENV', False)
    if virtualenv and os.path.exists(virtualenv):
        activate_this = os.path.join(virtualenv, 'bin/activate_this.py')
        if os.path.exists(activate_this):
            execfile(activate_this, dict(__file__=activate_this))

    os.environ['DJANGO_SETTINGS_MODULE'] = 'sara_cmt.settings'

    # Django 1.4+
    #from django.core.wsgi import get_wsgi_application
    #return get_wsgi_application()(environ, start_respone)
    
    try:
        # DJango 1.2
        import django.core.handlers.wsgi
        return django.core.handlers.wsgi.WSGIHandler()(environ, start_response)
    except ImportError:
        start_response('200 OK',[('Content-type','text/html')])
        return ['<html><body><h1>Unable to load CMT/Django environment!</h1></body></html>']
