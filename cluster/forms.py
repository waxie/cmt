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

from django import forms


class InterfaceForm(forms.ModelForm):
    """
    InterfaceForm.  Used to (override) size  of text input boxes

    If you don't set these sizes, django-admin/grappelli will use database field size
    for form field size. I.e.: CharField of max size 255 becomes Input field of 255 wide
    """

    class Meta:
        widgets = {  'label': forms.TextInput(attrs={'size': 10})
                    ,'aliases': forms.TextInput(attrs={'size': 10})
                    ,'ip': forms.TextInput(attrs={'size': 10})
                    ,'hwaddress': forms.TextInput(attrs={'size': 10})
                 }
# examples of other form widgets: PasswordInput, HiddenInput, Select, DateInput, files.
