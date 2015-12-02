# Django settings for cmt_server project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
AUTHENTICATION_ENABLED = True

import os, os.path, sys, ConfigParser, site, string

from socket import gethostbyname_ex
from exceptions import SystemExit

error_occured = False
error_messages = [ ]

CONFIG_DIR = None

where_am_i = os.path.dirname( __file__ )
devel_file = os.path.normpath(os.path.join( where_am_i, '.DEVELOPMENT' ) )

if os.path.exists( devel_file ):

    # Don't use system wide (production) config, but local development config
    CONFIG_FILE = os.path.normpath(os.path.join( where_am_i, 'cmt.conf') )
    CONFIG_DIR = where_am_i
    DEVELOPMENT_ENVIRONMENT = True
else:
    DEVELOPMENT_ENVIRONMENT = False

    # RB: config location finding logic due to stupid distutils
    for config_dir_guess in [ 'etc/cmt', 'local/etc/cmt' ]:

         if os.path.exists( os.path.join( site.sys.prefix, config_dir_guess ) ):

              CONFIG_DIR = os.path.join( site.sys.prefix, config_dir_guess )
              CONFIG_FILE = '%s/cmt.conf' % CONFIG_DIR
              break

if not CONFIG_DIR:

    err_str = "Unable to find config dir. Tried these path's:"
    print err_str

    error_messages.append( err_str )

    for config_dir_guess in [ 'etc/cmt', 'local/etc/cmt' ]:

        err_str = '- %s' %( os.path.join( site.sys.prefix, config_dir_guess ) )
        print err_str

        error_messages.append( err_str )

    raise SystemExit( string.join( error_messages, '\n') )

# Path's customizable through virtualenv
sample_configfile = '%s/cmt.conf.sample' % CONFIG_DIR

if not os.path.exists( CONFIG_FILE ):

    error_occured = True
    err_str = 'Unable to find config file: %s' %CONFIG_FILE
    print err_str

    error_messages.append( err_str )

    print ''
    print 'Fatal: Giving up and exiting now..'

    raise SystemExit( string.join( error_messages, '\n') )

config = ConfigParser.RawConfigParser()
config.read( CONFIG_FILE )

try:
    DATABASE_HOST       = config.get('database', 'HOST')
    DATABASE_ENGINE     = 'django.db.backends.' + config.get('database', 'ENGINE')
    DATABASE_NAME       = config.get('database', 'NAME')


except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

    error_occured = True
    err_msg = 'Config file error: %s' %str(details)
    print err_str

    error_messages.append( err_str )

    print ''
    print 'Fatal: Giving up and exiting now..'

    raise SystemExit( string.join( error_messages, '\n') )

try: # Optional
    DATABASE_PORT = config.get('database', 'PORT')

except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

    DATABASE_PORT = None

try: # Optional
    TEST_DATABASE_NAME = config.get('database', 'TEST_NAME')

except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

    TEST_DATABASE_NAME = None

try:
    gethostbyname_ex( DATABASE_HOST )

except socket.gaierror, details:

    error_occured = True
    err_msg = 'Unable to resolve database host: %s' %DATABASE_HOST
    print err_str

    error_messages.append( err_str )

    print ''
    print 'Giving up and exiting now..'

    raise SystemExit( string.join( error_messages, '\n') )

try:
    DATABASE_USER       = config.get('database', 'USER')

except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

    error_occured = True
    err_str = 'No option [database] USER'
    print err_str

    error_messages.append( err_str )

    print ''
    print 'Giving up and exiting now..'

    raise SystemExit( string.join( error_messages, '\n') )

try:
    DATABASE_PASSWORD   = config.get('database', 'PASSWORD')

except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

    error_occured = True
    err_str = 'No option [database] PASSWORD'
    print err_str

    error_messages.append( err_str )

    print ''
    print 'Giving up and exiting now..'

    raise SystemExit( string.join( error_messages, '\n') )

try:
    WEB_DOMAIN   = config.get('web', 'DOMAIN')

except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

    error_occured = True
    err_str = 'No option [web] DOMAIN'
    print err_str

    error_messages.append( err_str )

    print ''
    print 'Giving up and exiting now..'

    raise SystemExit( string.join( error_messages, '\n') )

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
    }
}

if DATABASE_PORT:
    DATABASES['default']['PORT'] = DATABASE_PORT

if TEST_DATABASE_NAME:
    DATABASES['default']['NAME'] = TEST_DATABASE_NAME

ALLOWED_HOSTS = [ 'localhost', '.' + WEB_DOMAIN ]

ADMINS = (
    ('Ramon Bastiaans', 'ramon.bastiaans@surfsara.nl'),
    ('Sil Westerveld', 'sil.westerveld@surfsara.nl')
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
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

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

## Absolute filesystem path to the directory that will hold user-uploaded files.
## Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), 'media'))
#
## URL that handles the media served from MEDIA_ROOT. Make sure to use a
## trailing slash.
## Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), 'static'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u#396z3t0s(@a2jvgs@%pbu$ytvhzzic70!*=x4cb9g-ae8_k_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'cmt_server.urls'

FILE_UPLOAD_TEMP_DIR = '/tmp'

TEMPLATE_DIRS = (
    FILE_UPLOAD_TEMP_DIR,
)

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)


FIXTURE_DIRS = (
    # A fixture is a collection of files that contain serialized contents of
    # the database. (can be used for testing)
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'fixtures')),
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Append your IP to use the debug_toolbar
INTERNAL_IPS = (
    '145.100.1.137',
    '2001:610:108:2031::15',
    '127.0.0.1',
)

GRAPPELLI_ADMIN_TITLE = 'Config Management Tool'

SMUGGLER_EXCLUDE_LIST = [ 'Group', 'User' ]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

GRAPPELLI_INDEX_DASHBOARD = 'cmt_server.dashboard.CustomIndexDashboard'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'PAGINATE_BY': 10,

    # Generic filtering backend that allows us to easily construct
    # complex searches and filters.
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    )
}

# <AUTH AGAINST LDAP> (based on http://packages.python.org/django-auth-ldap/)
#
if AUTHENTICATION_ENABLED:
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

    #AUTH_LDAP_CONNECTION_OPTIONS['ldap.OPT_TIMEOUT'] = '3000'

    # Keep ModelBackend around for per-user permissions and maybe a local
    # superuser.
    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [ 'rest_framework.authentication.BasicAuthentication' ]
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [ 'rest_framework.permissions.IsAuthenticated' ]
#
# </AUTH AGAINST LDAP>
#
#####

INSTALLED_APPS = (
    'django.contrib.sites',
    'rest_framework',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'grappelli.dashboard',
    'grappelli',
    'smuggler',
    'tagging',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'django.contrib.messages',
    'cmt_server.apps.cluster',
    #'debug_toolbar',
    'django_extensions'
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    #'debug_toolbar.panels.logger.LoggingPanel',
)

def custom_show_toolbar(request):
    return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
    'SHOW_TOOLBAR_CALLBACK': 'cmt_server.settings.custom_show_toolbar',
    #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
}

# Finally: test our django/database (settings)
from django.db import connection
from exceptions import *

try:
    c=connection.cursor()
except Exception as details:

    raise SystemExit( str( details ) )

print 'DATABASE SETTINGS:'
print 'host: %s | engine: %s | name: %s' %(DATABASE_HOST,DATABASE_ENGINE,DATABASE_NAME)
