#!/usr/bin/env python
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

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmt.settings")

if __name__ == "__main__":

    BASE_DIR = os.path.realpath(os.path.dirname(__file__))

    if os.path.isfile(os.path.join(BASE_DIR, '.virtual_env_path')):
        print('Setting up virtualenv environment')
        vpath = None
        with open(os.path.join(BASE_DIR, '.virtual_env_path'), 'r') as fi:
            vpath = fi.read().strip()

        if vpath:
            print('  using %s' % vpath)
            activate_this = os.path.join(vpath, 'bin/activate_this.py')
            if os.path.isfile(activate_this):
                execfile(activate_this, dict(__file__=activate_this))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
