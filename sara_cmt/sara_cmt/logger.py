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

import logging
import logging.config


class Logger:
    """
        A logging facility, implemented with the borg design pattern. Makes
        use of the Python logging lib, see:
            http://docs.python.org/library/logging.html
    """
    __shared_state = {}

    # Check for existence of a global logging object, otherwise make one
    if 'logger' not in __shared_state.keys():
        #TODO: think about a (better) way to make this dynamic:
        import site

        if site.sys.prefix in [ '/usr', '/' ]:
            ETC_PREPEND = ''
        else:
            ETC_PREPEND = site.sys.prefix

        logging.config.fileConfig('%s/etc/cmt/logging.conf'%ETC_PREPEND)
        __shared_state['logger'] = logging.getLogger('cli')

    def __init__(self):
        """
            Assigns the global __shared_state to __dict__ to be able to use
            the class like a singleton.
        """
        self.__dict__ = self.__shared_state

    def getLogger(self):
        """
            Returns the only logger instance (or state, to be exactly).
        """
        return self.__dict__['logger']
