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

import os, sys

# Append django-libs and directory which holds the sara_cmt project
sys.path.append('/var/lib/python-support/python%s/django'%sys.version[:3])

# Append SARA CMT specific paths
PROJECTPATH = os.path.normpath('/opt/sara_cmt')

sys.path.append(PROJECTPATH)
sys.path.append(os.path.join(PROJECTPATH,'site-packages')) # should be a symbolic link to (non-global) site-packages


os.environ['DJANGO_SETTINGS_MODULE'] = 'sara_cmt.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

