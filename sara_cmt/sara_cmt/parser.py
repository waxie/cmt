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

import optparse


class Parser:
    """
        Optionparser, implemented with the borg design pattern.
    """
    __shared_state = {}

    # Check for existence of a global parser object, otherwise make one
    if 'parser' not in __shared_state.keys():
        __shared_state['parser'] = optparse.OptionParser()

    def __init__(self):
        self.__dict__ = self.__shared_state

    def getParser(self):
        return self.__dict__['parser']
