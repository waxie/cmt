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

import logging, logging.config, settings, os.path

from exceptions import SystemExit

class Logger:
    """
        A logging facility, implemented with the borg design pattern. Makes
        use of the Python logging lib, see:
            http://docs.python.org/library/logging.html
    """
    __shared_state = {}

    # Check for existence of a global logging object, otherwise make one
    if 'logger' not in __shared_state.keys():

        if not os.path.exists( '%s/logging.conf' %settings.CONFIG_DIR ):

            raise SystemExit( 'Config file does not exist: %s/logging.conf' %settings.CONFIG_DIR )

        logging.config.fileConfig('%s/logging.conf' %settings.CONFIG_DIR )
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
