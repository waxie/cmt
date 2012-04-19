#from distutils.core import setup
from setuptools import setup
setup(
    name = 'CMT',
    version = '1.0',
    description = 'Cluster Management Tool',
    url = 'http://subtrac.sara.nl/oss/cmt/',
    #download_url = ''
    author = 'Sil Westerveld',
    author_email = 'sil.westerveld@sara.nl',
    license = 'GPL',
    long_description = '''\
CMT is a Cluster Management Tool originally created at SARA Computing and \
Networking Services, which is based in Amsterdam and known as SARA nowadays.''',

    platforms = ['linux-x86_64'],

    # see: http://pypi.python.org/pypi?:action=list_classifiers
    classifiers = [
        #'Development Status :: 4 - Beta',
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
# The packages option tells the Distutils to process (build, distribute, install, etc.) all pure Python modules found in each package mentioned in the packages list. In order to do this, of course, there has to be a correspondence between package names and directories in the filesystem. The default correspondence is the most obvious one, i.e. package distutils is found in the directory distutils relative to the distribution root. Thus, when you say packages = ['foo'] in your setup script, you are promising that the Distutils will find a file foo/__init__.py (which might be spelled differently on your system, but you get the idea) relative to the directory where your setup script lives.
#
    packages = ['', 'sara_cmt', 'sara_cmt.cluster', 'sara_cmt.cluster.templatetags'],
    #packages = ['sara_cmt', 'sara_cmt.cluster', 'sara_cmt.cluster.templatetags'],

# http://docs.python.org/distutils/setupscript.html#listing-individual-modules
# This describes two modules, one of them in the "root" package, the other in the pkg package. Again, the default package/directory layout implies that these two modules can be found in mod1.py and pkg/mod2.py, and that pkg/__init__.py exists as well.
#
#    py_modules = ['mod1', 'pkg.mod2'],
    #py_modules = ['cmt.py'],

# http://docs.python.org/distutils/setupscript.html#relationships-between-distributions-and-packages
# Dependencies on other Python modules and packages can be specified by supplying the requires keyword argument to setup(). The value must be a list of strings. Each string specifies a package that is required, and optionally what versions are sufficient.
#
    requires = ['Django (>=1.2)', 'IPy (>=0.75)', 'django_extensions (>=0.4)', 'django_tagging (>=0.3.1)', 'psycopg2 (>=2.4.4)', 'Python (>=2.6)'],
    #provides
    #obsoletes

    # http://docs.python.org/distutils/setupscript.html#installing-scripts
    #
    #scripts = ['cmt.py'],
    #scripts = ['cmt', 'cmt.py'],

    # http://docs.python.org/distutils/setupscript.html#installing-package-data
    # Often, additional files need to be installed into a package. These files are often data that's closely related to the package's implementation, or text files containing documentation that might be of interest to programmers using the package. These files are called package data.
    #package_data = {'': ['cmt', 'cmt.py'],},
    package_dir = {'sara_cmt': 'sara_cmt'},
    package_data = {'sara_cmt': ['apache/django.wsgi']},
)
#setup(
#    #maintainer = ''
#    #maintainer_email = ''
#
#    data_files = [('config', ['config/cmt.cfg'])],
#)
