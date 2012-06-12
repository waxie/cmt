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
    version = '1.0',
    description = 'Cluster Management Tool',
    url = 'http://subtrac.sara.nl/oss/cmt/',
    #download_url = ''
    author = 'Sil Westerveld',
    author_email = 'sil.westerveld@sara.nl',
    license = 'GPL',
    #long_description = open('README').read(),
    long_description = '''\
CMT is a Cluster Management Tool originally created at SARA Computing and \
Networking Services, which is based in Amsterdam and known as SARA nowadays.''',

    platforms = ['linux-x86_64'],

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

# http://docs.python.org/distutils/setupscript.html#listing-individual-modules
# This describes two modules, one of them in the "root" package, the other in the pkg package. Again, the default package/directory layout implies that these two modules can be found in mod1.py and pkg/mod2.py, and that pkg/__init__.py exists as well.
#
#    py_modules = ['mod1', 'pkg.mod2'],
    #py_modules = ['bin.cmt'],

# http://docs.python.org/distutils/setupscript.html#relationships-between-distributions-and-packages
# Dependencies on other Python modules and packages can be specified by supplying the requires keyword argument to setup(). The value must be a list of strings. Each string specifies a package that is required, and optionally what versions are sufficient.
#
    #
    # Somehow 'requires' doesn't work; dependencies won't be installed
    #requires = [
    #    'Django (>=1.2, <1.3)',
    #    'IPy (>=0.75)',
    #    'django_extensions (>=0.4)',
    #    'django_tagging (>=0.3.1)',
    #    'psycopg2 (>=2.4.4)',
    #    'Python (>=2.6)'
    #],
    install_requires = [
        'Django>=1.2, <1.3',
        'IPy>=0.75',
        'django_extensions>=0.4',
        'django_tagging>=0.3.1',
        'psycopg2>=2.4.4',
        'Python>=2.6'
    ],
    #provides =
    #obsoletes =

    # http://docs.python.org/distutils/setupscript.html#installing-scripts
    #
    #scripts = ['sara_cmt/cmt.py'],
    scripts = ['bin/cmt'],

    # http://docs.python.org/distutils/setupscript.html#installing-package-data
    # Often, additional files need to be installed into a package. These files are often data that's closely related to the package's implementation, or text files containing documentation that might be of interest to programmers using the package. These files are called package data.
    #package_dir = {'sara_cmt': 'sara_cmt'},
    #package_data = {'sara_cmt': ['sara_cmt/apache/django.wsgi']},

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
            'templates/examples/base_allnodes.cmt',
            'templates/examples/cnames.cmt',
            'templates/examples/first_test.cmt',
            'templates/examples/gina_allnodes.cmt',
            'templates/examples/header',
            'templates/examples/lisa_allnodes.cmt'
        ]),
        # executable
        ('bin/', ['bin/cmt']),
    ]
)
