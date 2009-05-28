import os, sys
# Append django-libs and directory which holds the sara_cmt project
sys.path.append('/var/lib/python-support/python%s/django'%sys.version[:3])
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../..'))) # was: sys.path.append('/home/sil/checkouts/beowulf/trunk/sara_cmt/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sara_cmt.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

