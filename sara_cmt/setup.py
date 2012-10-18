#    This file is part of CMT, a Cluster Management Tool made at SARA.
#    Copyright (C) 2012  Sil Westerveld
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
import site

ETC_PREPEND = ''

if site.sys.prefix in [ '/usr', '/' ]:
    ETC_PREPEND = '/'

setup(
    name = 'CMT',
    version = '1.0.1',
    description = 'Cluster Management Tool',
    url = 'http://subtrac.sara.nl/oss/cmt/',
    #download_url = ''
    author = 'CMT Development team',
    author_email = 'cmt-users@lists.osd.sara.nl',
    license = 'GPL',
    #long_description = open('README').read(),
    long_description = 'CMT is a Cluster Management Tool originally created '\
        'at SARA Computing and Networking Services, which is based in'\
        'Amsterdam and known as SARA nowadays.',

    platforms = ['linux-x86_64', 'linux-i386' ],

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



# http://docs.python.org/distutils/setupscript.html#listing-whole-packages
    #packages = ['sara_cmt', 'sara_cmt/sara_cmt', 'sara_cmt/sara_cmt.cluster', 'sara_cmt/sara_cmt.cluster.templatetags'],
    packages = ['sara_cmt', 'sara_cmt.cluster', 'sara_cmt.cluster.templatetags'],

# http://docs.python.org/distutils/setupscript.html#relationships-between-distributions-and-packages
# Dependencies on other Python modules and packages can be specified by supplying the requires keyword argument to setup(). The value must be a list of strings. Each string specifies a package that is required, and optionally what versions are sufficient.
#
    #
    # Somehow 'requires' doesn't work; dependencies won't be installed
    #requires = [
    #    'Python (>=2.6)'
    #    'Django (>=1.2, <1.3)',
    #    'IPy (>=0.75)',
    #    'django_extensions (>=0.4)',
    #    'django_tagging (>=0.3.1)',
    #    'psycopg2 (>=2.4.4)',
    #],
    install_requires = [
        'djangorestframework',
        'Python>=2.6',
        'Django>=1.3',
        'IPy>=0.75',
        'django_extensions>=0.4',
        'django_tagging>=0.3.1',
        'psycopg2>=2.4.4'
    ],

    # http://docs.python.org/distutils/setupscript.html#installing-scripts
    #
    #scripts = ['sara_cmt/cmt.py'],
    scripts = ['bin/cmt'],

    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    # The data_files option can be used to specify additional files needed by the module distribution: configuration files, message catalogs, data files, anything which doesn't fit in the previous categories.
    # data_files specifies a sequence of (directory, files) pairs in the following way:
    #     data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #             ('/etc/init.d', ['init-script'])]
    #
    # NOTE: wildcards aren't accepted here
    data_files = [
        # config-files
        (ETC_PREPEND + 'etc/cmt/', [
            'etc/cmt.conf.sample',
            'etc/logging.conf'
        ]),
        # empty directory for CMT-templates
        (ETC_PREPEND + 'etc/cmt/templates', []),
        # examples of CMT-templates
        ('share/doc/cmt/templates/examples', [
            'templates/examples/simple_cnames.cmt',
            'templates/examples/simple_hostnames.cmt',
            'templates/examples/simple_dhcpd.conf.cmt',
            'templates/examples/complex_dns.cmt'
        ]),
        # executable
        (ETC_PREPEND + 'bin/', ['bin/cmt']),
    ]
)
