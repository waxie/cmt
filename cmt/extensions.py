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

from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from tagging.fields import TagField


class ModelExtension(models.Model):
    tags = TagField()
    created_on = CreationDateTimeField()
    updated_on = ModificationDateTimeField()
    note = models.TextField(blank=True)

    class Meta:
        abstract = True