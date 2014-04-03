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
from cmt_client import __version__

setup(
    name = 'cmt-client',
    version = __version__,
    description = 'Cluster Management Tool',
    url = 'http://oss.trac.sara.nl/cmt/',
    author = 'CMT Development team',
    author_email = 'cmt-users@lists.osd.sara.nl',
    license = 'GPL',
    long_description = 'CMT is a Cluster Management Tool originally created at SURFsara.',

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

    packages = [ 'cmt_client.apps.cli' ],

    install_requires = [
        'Python>=2.6.0','Python<3.0'
    ],

    # Only way to get something installed with mode 755 ...
    scripts = [ 'bin/cmt' ],

    # data_files = ( target_dir, source_files )
    # if target_dir is not absolute, will use site.sys.prefix
    data_files = [

        # config-files
        ( 'etc/cmt', [
            'etc/cmt.conf.sample',
            'etc/logging.conf'
        ]),

        # templates
        ( 'etc/cmt/templates', [
            'templates/examples/README'
        ]),

        # examples of CMT-templates
        ( 'etc/cmt/templates/examples', [
            'templates/examples/simple_cnames.cmt',
            'templates/examples/simple_hostnames.cmt',
            'templates/examples/simple_dhcpd.conf.cmt',
            'templates/examples/complex_dns.cmt'
        ])
    ]
)
