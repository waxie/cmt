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
# examples of other form widgets: PasswordInput, HiddenInput, Select, DateInput, etc.
