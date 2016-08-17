# Django settings for cmt_server project.

import os
from exceptions import SystemExit

from cmt.configuration import Configuration

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

KNOWN_CONFIG_PATHS = [
    '/etc/cmt',
    '/usr/etc/cmt',
    os.path.realpath(os.path.join(BASE_DIR, '../', 'conf')),
    os.path.join(BASE_DIR, 'files'),
]

CONFIG_DIR = None
CONFIG_FILE = None

for config_dir in KNOWN_CONFIG_PATHS:
    if os.path.isdir(config_dir) and os.path.exists(os.path.join(config_dir, 'cmt.conf')):
        CONFIG_DIR = config_dir
        CONFIG_FILE = os.path.join(config_dir, 'cmt.conf')
        break

if not CONFIG_DIR or not CONFIG_FILE:
    raise SystemExit("Unable to continue, missing config_dir and config_file for this instance")

config = Configuration(CONFIG_FILE)

DEBUG = config.getboolean('web', 'debug')
LDAP_AUTHENTICATION = config.getboolean('web', 'ldap_auth')
SECRET_KEY = 'u#396z3t0s(@a2jvgs@%pbu$ytvhzzic70!*=x4cb9g-ae8_k_'

DATABASES = {
    'default': config.get_db_config()
}

ALLOWED_HOSTS = config.get_allowed_hosts()

ADMINS = config.get_admins()
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
ROOT_URLCONF = 'cmt.urls'

# Do not load multi-language support
USE_I18N = False

# But support multiple timezones
USE_L10N = True

# Where are my static stuff
STATIC_ROOT = os.path.realpath(os.path.join(BASE_DIR, '../', 'htdocs/static')) 
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'cmt', 'static'),
)

# File upload
FILE_UPLOAD_TEMP_DIR = '/tmp'

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

# Template config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            FILE_UPLOAD_TEMP_DIR,
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
            'debug': DEBUG,
        }
    }
]

# Middleware classes
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Logging
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

INSTALLED_APPS = (
    # Public apps/projects
    'rest_framework',
    'django_extensions',
    'smuggler',
    'tagging',
    'grappelli.dashboard',
    'grappelli',

    # Django apps
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'django.contrib.messages',

    # CMT apps
    'cluster',
    'api',
    'client',
)

# Which auth backends must we support
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# django-auth-ldap
if LDAP_AUTHENTICATION:
    AUTHENTICATION_BACKENDS = ('django_auth_ldap.backend.LDAPBackend',) + AUTHENTICATION_BACKENDS

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

    # Only users in this group can log in.
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

    # AUTH_LDAP_CONNECTION_OPTIONS['ldap.OPT_TIMEOUT'] = '3000'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': (
        'rest_framework.serializers.HyperlinkedModelSerializer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    'PAGE_SIZE': 100,

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # Generic filtering backend that allows us to easily construct
    # complex searches and filters.
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),

    # Be compatible with the current API
    'COMPACT_JSON': False
}

# Grappelli configuration
GRAPPELLI_INDEX_DASHBOARD = 'cmt.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'Config Management Tool'

# Smuggler
SMUGGLER_EXCLUDE_LIST = [ 'Group', 'User' ]

CLIENT_SKIP_MODELS = [
    'equipment_role',
    'company_addresses'
]
CLIENT_API_VERSION = 'v1'

import logging
logger = logging.getLogger('django')   # Django's catch-all logger
hdlr = logging.StreamHandler()   # Logs to stderr by default
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)
