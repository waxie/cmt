
import os


# Documentation of settings can be found on:
#
#   http://docs.djangoproject.com/en/dev/ref/settings/

SARACMT_BASE = os.path.normpath(os.path.dirname(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(SARACMT_BASE, os.path.pardir))

# Set to True for CMT clients, or False for the CMT server
CLIENT_ONLY = True

# Whether or not to set logging to debug-level
DEBUG = True

ADMINS = (
    ('Sil Westerveld', 'sil.westerveld@sara.nl'),
    #('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# The database settings are imported, due to confidential data which should be
# excluded from the SVN repository. An example of the needed info for database
# configuration is commented out.
# DATABASE_ENGINE    = 'postgresql_psycopg2'
# DATABASE_NAME      = 'my_database'
# DATABASE_USER      = 'db_user'
# DATABASE_PASSWORD  = 'secret'
# DATABASE_HOST      = 'database.example.com'
from settings_db import *



#####
#
# <AUTH AGAINST LDAP> (based on http://packages.python.org/django-auth-ldap/)
#
if not CLIENT_ONLY:
    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType


    # Baseline configuration.
    AUTH_LDAP_SERVER_URI = "ldaps://ldap.cua.sara.nl"

    # Set AUTH_LDAP_USER_DN_TEMPLATE to a template that will produce the
    # authenticating user's DN directly. This template should have one
    # placeholder, %(user)s.
    AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=Users,dc=hpcv,dc=sara,dc=nl'

    # Set up the basic group parameters.
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch('ou=Groups,dc=hpcv,dc=sara,dc=nl',
        ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)',
    )
    AUTH_LDAP_GROUP_TYPE = PosixGroupType()

    ## Only users in this group can log in.
    AUTH_LDAP_REQUIRE_GROUP = 'cn=cmt,ou=Groups,dc=hpcv,dc=sara,dc=nl'

    # Populate the Django user from the LDAP directory.
    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        'is_active': 'cn=cmt,ou=Groups,dc=hpcv,dc=sara,dc=nl',
        'is_staff': 'cn=cmt,ou=Groups,dc=hpcv,dc=sara,dc=nl',
        'is_superuser': 'cn=cmt,ou=Groups,dc=hpcv,dc=sara,dc=nl',
    }

    # This is the default, but I like to be explicit.
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    # Cache group memberships for an hour to minimize LDAP traffic
    AUTH_LDAP_CACHE_GROUPS = True
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'sara_cmt.urls'

# Templates for the CMT command line interface.
# (thus, the templates for our configfiles, etc)
CMT_TEMPLATES_DIR = '/etc/sara_cmt/templates'

# Templates for the CMT web-frontend.
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'cluster/templates')),
    CMT_TEMPLATES_DIR,
)

FIXTURE_DIRS = (
    # A fixture is a collection of files that contain serialized contents of
    # the database. (can be used for testing)
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'fixtures')),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.webdesign',
    'piston',
    'sara_cmt.cluster',
    'sara_cmt.api',
    'django_extensions',
    'tagging',
    'south',
    'debug_toolbar',
)

# Append your IP to use the debug_toolbar
#  '145.100.6.163',
INTERNAL_IPS = (
    '127.0.0.1',
)
