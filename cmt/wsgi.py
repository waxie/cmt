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
#  Alias /static  /path/to/virtualenvs/cmt/lib/python<ver>/site-packages/server/static
#

import os
import sys

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(BASE_DIR)

if os.path.isfile(os.path.join(BASE_DIR, '.virtual_env_path')):
    vpath = None
    with open(os.path.join(BASE_DIR, '.virtual_env_path'), 'r') as fi: 
        vpath = fi.read().strip()

    if vpath:
        activate_this = os.path.join(vpath, 'bin/activate_this.py')
        if os.path.isfile(activate_this):
            execfile(activate_this, dict(__file__=activate_this))


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmt.settings")

application = get_wsgi_application()

