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

