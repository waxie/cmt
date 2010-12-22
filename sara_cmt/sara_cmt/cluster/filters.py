from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec, DateFieldFilterSpec
#from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from datetime import date, timedelta

class InSupportFilterSpec(DateFieldFilterSpec):
    """
        Adds filtering by warranty-status values in the admin filter sidebar.
        Set the in_support_filter filter in the model field attribute
        'in_support_filter'.
        
        my_model_field.in_support_filter = True
    """

    def __init__(self, f, request, params, model, model_admin):
        super(InSupportFilterSpec, self).__init__(f, request, params, model, model_admin)
        
        today = date.today()
        days_thirty = today + timedelta(30)
        self.links = (
            (_('All'), {}),
            (_('In Support'), {'%s__gte' % self.field.name: str(today), }),
            (_('Expiring in 30 days'), {'%s__gte' % self.field.name: str(today), '%s__lte' % self.field.name: str(days_thirty) }),
            (_('Expired'), {'%s__lte' % self.field.name: str(today), }),
        )

    def title(self):
        return 'warranty status'

# register the filter
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'in_support_filter', False), InSupportFilterSpec))
