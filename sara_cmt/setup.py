#!/usr/bin/env python

from distutils.core import setup
from sara_cmt import settings

setup(
    name = 'saracmt',
    version = '0.9',
    author = 'Sil Westerveld',
    author_email = 'sil.westerveld@sara.nl',
    url = 'cmt.hpcv.sara.nl/doc',
    description = 'SARA Cluster Management Tool',
    long_description = '''SARA CMT is a Cluster Management Tool, developed and used \
      at SARA Computing & Networking Services. Main purpose is to automagicaly \
      generate and save config-files based on Django-like templates.''',

    classifiers = [
        'Development Status :: Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License ::  OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.6',
        'Topic :: System :: System Administration',
    ],

    #platforms
    license = 'GPL',
    packages = ['config', 'sara_cmt', 'sara_cmt.cluster', 'sara_cmt.cluster.templatetags'],
    #package_data = {'sara_cmt': ['*']},
    scripts = ['cmt'],
    #data_files = [],
    requires = ['django', 'django_extensions', 'south', 'debug_toolbar', 'IPy'],
)
