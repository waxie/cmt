import os

SARACMT_BASE = os.path.normpath(os.path.dirname(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(SARACMT_BASE, os.path.pardir))

#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  #('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# The database settings are imported, due to confidential data which should be
# excluded from the SVN repository. An example of the needed info for database
# configuration is commented out.
import settings_db
#DATABASE_ENGINE    = '' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME      = '' # Or path to database file if using sqlite3.
#DATABASE_USER      = '' # Not used with sqlite3.
#DATABASE_PASSWORD  = '' # Not used with sqlite3.
#DATABASE_HOST      = '' # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT      = '' # Set to empty string for default. Not used with sqlite3.
#TEST_DATABASE_NAME = ''


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
  #path.normpath(path.join(CMTS_PATH, 'templates')),
  'templates',
  #os.path.join(os.path.dirname(__file__), 'templates'),
)

FIXTURE_DIRS = (
  # A fixture is a collection of files that contain serialized contents of the database.
  os.path.normpath(os.path.join(os.path.dirname(__file__), 'fixtures')),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.webdesign',
    'sara_cmt.cluster',
    'sara_cmt.django_cli',
    'tagging',
    'south',
)
