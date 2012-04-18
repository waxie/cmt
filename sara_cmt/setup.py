from distutils.core import setup
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



# The packages option tells the Distutils to process (build, distribute, install, etc.) all pure Python modules found in each package mentioned in the packages list. In order to do this, of course, there has to be a correspondence between package names and directories in the filesystem. The default correspondence is the most obvious one, i.e. package distutils is found in the directory distutils relative to the distribution root. Thus, when you say packages = ['foo'] in your setup script, you are promising that the Distutils will find a file foo/__init__.py (which might be spelled differently on your system, but you get the idea) relative to the directory where your setup script lives.
#
    packages = ['sara_cmt', 'sara_cmt.cluster', 'sara_cmt.cluster.templatetags'],

# This describes two modules, one of them in the "root" package, the other in the pkg package. Again, the default package/directory layout implies that these two modules can be found in mod1.py and pkg/mod2.py, and that pkg/__init__.py exists as well.
#
#    py_modules = ['mod1', 'pkg.mod2'],

# Dependencies on other Python modules and packages can be specified by supplying the requires keyword argument to setup(). The value must be a list of strings. Each string specifies a package that is required, and optionally what versions are sufficient.
#
    requires = ['Django (>=1.2)', 'IPy (>=0.75)', 'django_extensions (>=0.4)', 'django_tagging (>=0.3.1)', 'psycopg2 (>=2.4.4)', 'Python (>=2.6)'],

)
#setup(
#    #maintainer = ''
#    #maintainer_email = ''
#
#    scripts = ['cmt'],
#    data_files = [('config', ['config/cmt.cfg'])],
#)
