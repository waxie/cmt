import os

# Documentation of settings can be found on:
#
#   http://docs.djangoproject.com/en/dev/ref/settings/

SARACMT_BASE = os.path.normpath(os.path.dirname(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(SARACMT_BASE, os.path.pardir))

#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  ('Sil Westerveld', 'sil.westerveld@sara.nl'),
  #('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# The database settings are imported, due to confidential data which should be
# excluded from the SVN repository. An example of the needed info for database
# configuration is commented out.
from settings_db import *
#TEST_DATABASE_NAME = ''



#####
#
# <AUTH AGAINST LDAP>
#
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# (based on docs on http://packages.python.org/django-auth-ldap/)

# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldaps://master.cua.sara.nl"

# If you can't search anonymously, you can set AUTH_LDAP_BIND_DN to the
# distinguished name of an authorized user and AUTH_LDAP_BIND_PASSWORD to the
# password.
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

# This will perform an anonymous bind, search under
# "ou=users,dc=example,dc=com" for an object with a uid matching the user's
# name, and try to bind using that DN and the user's password. The search must
# return exactly one result or authentication will fail.
#AUTH_LDAP_USER_SEARCH = LDAPSearch('ou=Users,dc=hpcv,dc=sara,dc=nl',
#  ldap.SCOPE_SUBTREE, '(uid=%(user)s)'
#)
# To skip the search phase, set AUTH_LDAP_USER_DN_TEMPLATE to a template that
# will produce the authenticating user's DN directly. This template should have
# one placeholder, %(user)s. If the previous example had used
# ldap.SCOPE_ONELEVEL, the following would be a more straightforward (and
# efficient) equivalent:
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=Users,dc=hpcv,dc=sara,dc=nl'

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch('ou=Groups,dc=hpcv,dc=sara,dc=nl',
  ldap.SCOPE_SUBTREE, '(objectClass=groupOfNames)'
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

# Only users in this group can log in.
AUTH_LDAP_REQUIRE_GROUP = 'cn=hpcv_admin,ou=Groups,dc=hpcv,dc=sara,dc=nl'

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
  'first_name': 'givenName',
  'last_name': 'sn',
  'email': 'mail'
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
  'is_active': 'cn=hpcv_admin,ou=Groups,dc=hpcv,dc=sara,dc=nl',
  'is_staff': 'cn=hpcv_admin,ou=Groups,dc=hpcv,dc=sara,dc=nl',
  'is_superuser': 'cn=hpcv_admin,ou=Groups,dc=hpcv,dc=sara,dc=nl'
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = False # True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
  'django_auth_ldap.backend.LDAPBackend',
  'django.contrib.auth.backends.ModelBackend',
)
#
# </AUTH AGAINST LDAP>
#
#####





# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uygv6wrel4o2%x8s4dk2%i6=dp!2bt32$0ne-%_7&j=ez*u$1b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.load_template_source',
  'django.template.loaders.app_directories.load_template_source',
  #'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'sara_cmt.urls'

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  'templates',
)

FIXTURE_DIRS = (
  # A fixture is a collection of files that contain serialized contents of the database.
  os.path.normpath(os.path.join(os.path.dirname(__file__), 'fixtures')),
)


INSTALLED_APPS = (
#    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.webdesign',
    'sara_cmt.cluster',
    'sara_cmt.django_cli',
    'django_extensions',
    'tagging',
    'south',
)
