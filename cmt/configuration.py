#
# This file is part of CMT
#
# CMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# CMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMT.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2017 SURFsara

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

configparser.DEFAULTSECT = 'general'

REQUIRED_OPTIONS = {
    'database': ['engine', 'name', 'user', 'password', 'host'],
    'web': ['allowed_hosts', 'admins', 'debug'],
    'ldap': ['enabled', 'uri', 'bind_dn', 'bind_password', 'user_dn', 'group_dn', 'superuser_groups', 'staff_groups']
}

class Configuration(configparser.SafeConfigParser):

    def __init__(self, config_file):
        configparser.SafeConfigParser.__init__(self)
        self.read([config_file])
        self.__verify_configuration()

    def __verify_configuration(self):

        for section, options in REQUIRED_OPTIONS.items():
            if not self.has_section(section):
                raise SystemExit('Missing required configuration section %s' % section)

            for option in options:
                if not self.has_option(section, option):
                    raise SystemExit('Missing required option %s in section %s' % (option, section))

    def get_db_config(self):

        basic_config = {
            'ENGINE': 'django.db.backends.%s' % self.get('database', 'engine'),
            'NAME': self.get('database', 'name'),
            'USER': self.get('database', 'user'),
            'PASSWORD': self.get('database', 'password'),
            'HOST': self.get('database', 'host'),
        }

        if self.has_option('database', 'port') and self.getint('database', 'port'):
            basic_config['PORT'] = self.getint('database', 'port')

        if self.has_option('database', 'test_name') and self.get('database', 'test_name'):
            basic_config['NAME'] = self.getint('database', 'test_name')

        return basic_config

    def get_allowed_hosts(self):
        return [ x.strip() for x in self.get('web', 'allowed_hosts').split(',') ]

    def get_admins(self):

        admins = list()
        for pair in self.get('web', 'admins').split(';'):
            parts = pair.strip().split(';')
            if not len(parts) == 2:
                continue
            list.append([pair[0], pair[1]])

        return tuple(admins)

    def get_ldap_groups(self, types):

        allowed_groups = list()
        for t in types:
            allowed_groups += [ 'cn=%s,%s' % (x.strip(), self.get('ldap', 'group_dn')) for x in self.get('ldap', t).split(',') ]

        return allowed_groups
