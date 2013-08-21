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

import os, os.path, sys, ConfigParser, site, string, time

from socket import gethostbyname_ex

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

if not CONFIG_DIR:

    print "Unable to find config dir. Tried these path's:"

    for config_dir_guess in [ 'etc/cmt', 'local/etc/cmt' ]:

        print '- %s' %( os.path.join( site.sys.prefix, config_dir_guess ) )

    print 'Exiting..'
    sys.exit( 1 )


# Path's customizable through virtualenv
sample_configfile = '%s/cmt.conf.sample' % CONFIG_DIR

prompt_settings = []

def count_configlines( filename ):

	line_count	= 0
	cfg_fp		= open( filename )

	for line in cfg_fp.readlines():

		line = line.strip()

		if len( line ) == 0:
			continue

		# RB: ConfigParser considers lines starting with # or ; as comments
		if line[0] == '#' or line[0] == ';':
			continue

		line_count += 1

	cfg_fp.close()

	return line_count

if not os.path.exists( CONFIG_FILE ):

	print 'Unable to find config file: %s' %CONFIG_FILE

	if os.path.exists( sample_configfile ) and not DEVELOPMENT_ENVIRONMENT:

		print ''
		print 'Please modify the sample config file: %s to reflect your settings' %sample_configfile
		print 'and then rename it to: %s' %CONFIG_FILE

	else:

		print ''
		print 'Also no sample config file was found: %s' %sample_configfile
		print 'Something is terribly wrong here ;)'

	print ''
	print 'Fatal: Giving up and exiting now..'

	sys.exit(1)

# We are still here: both configfile AND sample_configfile found
if os.path.exists( sample_configfile ) and not DEVELOPMENT_ENVIRONMENT:

	# Is the sample configfile newer?
	if os.path.getmtime( sample_configfile ) > os.path.getmtime( CONFIG_FILE ):

		# Well this is weird, but not fatal
		print 'Warning: sample config file(%s) is newer than original config(%s)' %(sample_configfile, CONFIG_FILE )

		# Does the sample config file contain more options?
		if count_configlines( sample_configfile ) > count_configlines( CONFIG_FILE ):

			print 'Warning: sample config file contains MORE OPTIONS than original config!'
			print ''
			print 'This happens for example if you upgraded CMT and the new release incorporates new configuration options!'
			print ''
			print 'Please update your original config(%s) to incorporate the new config options from sample config(%s)' %( CONFIG_FILE, sample_configfile )
			print ''

		# Give them some time to think about warnings and generally annoy them just enough to fix it
		time.sleep(2)

		# Moving right along; print empty line for cosmetic reasons
		print ''

config = ConfigParser.RawConfigParser()
config.read( CONFIG_FILE )

try:
	DATABASE_HOST		= config.get('database', 'HOST')
	DATABASE_ENGINE		= config.get('database', 'ENGINE')
	DATABASE_NAME		= config.get('database', 'NAME')
	
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError), details:

	print 'Config file error: %s' %str(details)
	print ''
	print 'Giving up and exiting now..'
	sys.exit(1)

try: # Optional
	DATABASE_PORT = config.get('database', 'PORT')

except ConfigParser.NoOptionError, details:

	pass

try: # Optional
	TEST_DATABASE_NAME = config.get('database', 'TEST_NAME')

except ConfigParser.NoOptionError, details:

	pass

try:
	gethostbyname_ex( DATABASE_HOST )

except socket.gaierror, details:

	print 'Unable to resolve database host: %s' %DATABASE_HOST
	print ''
	print 'Giving up and exiting now..'
	sys.exit(1)

try:
	DATABASE_USER		= config.get('database', 'USER')


except ConfigParser.NoOptionError, details:

	prompt_settings.append( ('DATABASE_USER', 'Username: ', False) )

try:
	DATABASE_PASSWORD	= config.get('database', 'PASSWORD')

except ConfigParser.NoOptionError, details:

	prompt_settings.append( ('DATABASE_PASSWORD', 'Password: ', True) )

for prompt_list in prompt_settings:

	from getpass import getpass

	( prompt_value, input_text, input_hidden ) = prompt_list
	temp_val = ''

	if not input_hidden:

		temp_val = raw_input( input_text )
	else:
		temp_val = getpass( input_text )

	globals()[prompt_value] = temp_val

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        #'PORT': DATABASE_PORT,
    }
}

# Documentation of settings can be found on:
#
#   http://docs.djangoproject.com/en/dev/ref/settings/

# Only set CLIENT_ONLY to False on the central CMT-server
CLIENT_ONLY = True

DEBUG = False

ADMINS = (
    ('Sil Westerveld', 'sil.westerveld@sara.nl'),
    #('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

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

## Absolute path to the directory that holds media.
## Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''
#
## URL that handles the media served from MEDIA_ROOT. Make sure to use a
## trailing slash if there is a path component (optional in other cases).
## Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = ''

# Static files (replaces adminmedia from Django 1.3)
STATIC_ROOT = ''
STATIC_PATH = ''
STATIC_URL = '/media/'

## URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
## trailing slash.
## Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uygv6wrel4o2%x8s4dk2%i6=dp!2bt32$0ne-%_7&j=ez*u$1b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.load_template_source',
    #'django.template.loaders.app_directories.load_template_source',
    #'django.template.loaders.eggs.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'
#ROOT_URLCONF = 'sara_cmt.urls'

# Templates for the CMT command line interface.
# (thus, the templates for our configfiles, etc)
#TODO: think about a (better) way to make this dynamic:
#TODO: get this out of the settings.py, since it should be in the client config
CMT_TEMPLATES_DIR = '%s/templates' % CONFIG_DIR

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
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'sara_cmt.cluster',
    'django_extensions',
    'tagging',
)

if not CLIENT_ONLY:
    INSTALLED_APPS = INSTALLED_APPS + (
    'south', )

    SOUTH_DATABASE_ADAPTERS = {'default':'south.db.postgresql_psycopg2'}

# Append your IP to use the debug_toolbar
INTERNAL_IPS = (
    #'145.100.6.163',
    '127.0.0.1',
)
