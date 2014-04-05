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

from distutils.core import setup
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

    packages = [ 'cmt_server', 'cmt_server.apps', 'cmt_server.apps.cluster', 'cmt_server.apps.cluster.templatetags', 'cmt_server.apps.api'],

    install_requires = [
        'djangorestframework>=2.3.6',
        'Python<3.0.0,>=2.6.0',
        'Django<1.6.0,>=1.5.2',
        'IPy>=0.80',
        'django_extensions>=1.1.1',
        'psycopg2>=2.4.6',
        'django-grappelli<2.5.0,>=2.4.9',
        'django-smuggler',
        'feedparser'
    ],

    # data_files = ( target_dir, source_files )
    # if target_dir is not absolute, will use site.sys.prefix
    data_files = [

        # config-files
        ( 'etc/cmt', [
            'etc/cmt/cmt.conf.sample',
            'etc/cmt/logging.conf'
        ])

    ]
)
