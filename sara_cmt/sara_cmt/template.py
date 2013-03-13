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

from django.template import Template

from sara_cmt.logger import Logger
logger = Logger().getLogger()


class CMTTemplate(Template):
    """
        CMTTemplate adds some smart functionalities to the Django Template.
    """

    def __init__(self, template_string, origin=None, \
                 name='<Unknown Template>'):
        """
            Wraps Template.__init__()
        """
        logger.info('Initializing CMT Template')
        Template.__init__(self, template_string, origin, name)

        logger.info('CMT Template has been initialized')

    def render(self, context):
        rendered = super(CMTTemplate, self).render(context)
        return rendered
