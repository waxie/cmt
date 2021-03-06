#
# This file is part of CMT
#
# CMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# CMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMT.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2017 SURFsara

# Django settings for cmt_server project.

import os

from cmt.configuration import Configuration

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

VERSION = '2.5.0'

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
LDAP_AUTHENTICATION = config.getboolean('ldap', 'enabled')
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
LOGIN_URL = '/admin/login'

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
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
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
    'formatters': {
        'verbose': {
            'format' : '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt' : '%d/%b/%Y %H:%M:%S'
        },
        'simple' : {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': config.get('logging', 'filename'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARN',
            'propagate': True
        },
        'django_auth_ldap': {
            'handlers': ['file'],
            'level': 'WARN',
            'propagate': True
        },
        'cmt': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

INSTALLED_APPS = (
    # Public apps/projects
    'rest_framework',
    'django_extensions',
    'django_filters',
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

    AUTH_LDAP_GROUP_TYPE = PosixGroupType()

    # Baseline configuration.
    AUTH_LDAP_SERVER_URI = config.get('ldap', 'uri') 
    
    AUTH_LDAP_BIND_DN = config.get('ldap', 'bind_dn')
    AUTH_LDAP_BIND_PASSWORD = config.get('ldap', 'bind_password')

    AUTH_LDAP_USER_SEARCH = LDAPSearch(config.get('ldap', 'user_dn'), ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(config.get('ldap', 'group_dn'), ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)')

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        'is_active': config.get_ldap_groups(['staff_groups', 'superuser_groups']),
        'is_staff': config.get_ldap_groups(['staff_groups']),
        'is_superuser': config.get_ldap_groups(['superuser_groups']),
    }

    AUTH_LDAP_CACHE_GROUPS = True
    AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': (
        'rest_framework.serializers.HyperlinkedModelSerializer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
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
GRAPPELLI_ADMIN_TITLE = 'CMT %s' % VERSION

# Smuggler
SMUGGLER_EXCLUDE_LIST = ['Group', 'User']

# CMT Client options
CLIENT_SKIP_MODELS = [
    'equipment_role',
    'company_addresses'
]
CLIENT_API_VERSION = 'v2'
