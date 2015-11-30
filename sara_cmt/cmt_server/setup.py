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

from setuptools import setup, find_packages
from cmt_server import __version__

setup(
    name = 'cmt-server',
    version = __version__,
    description = 'Cluster Management Tool server',
    url = 'http://oss.trac.sara.nl/cmt/',
    author = 'CMT Development team',
    author_email = 'cmt-users@lists.osd.sara.nl',
    license = 'GPL',
    long_description = 'API and Web Admin server for the Cluster Management Tool',

    include_package_data = True,
    zip_safe = False,

    platforms = [ 'linux-x86_64', 'linux-i386' ],

    # see: http://pypi.python.org/pypi?:action=list_classifiers
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: System Administrators',
        'License ::  OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Topic :: Database :: Front-Ends',
        'Topic :: System :: Clustering',
        'Topic :: System :: System Administration',
        'Topic :: Utilities',
    ],

    packages = find_packages(),

    install_requires = [
        'Python<3.0.0,>=2.7.0',
        'Django<1.9.0,<1.8.6,>1.8.6',
        'djangorestframework<3.0.0,>=2.3.0',
        'django-grappelli<2.8.0,>=2.7.0',
        'django_extensions',
        'django-smuggler',
        'django-auth-ldap',
        'django-debug-toolbar',
        'django-filter',
        'psycopg2',
        'IPy',
        'feedparser'
    ],

    # data_files = ( target_dir, source_files )
    # if target_dir is not absolute, will use site.sys.prefix
    data_files = [

        # config-files
        ( 'etc/cmt', [
            'etc/cmt/cmt.conf.sample',
            'etc/cmt/logging.conf'
        ]),

        ( 'wsgi', [
            'wsgi/cmt.wsgi'
        ])
    ]
)
