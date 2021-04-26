# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.contrib import admin

# Our modules
from runtest.models import Parameter
from .version_model_admin import VersionModelAdmin
from runtest.forms.parameter import ParameterForm

class ParameterAdmin(VersionModelAdmin):
    """
    We inherit from this class so that it will automatically insert the last version field
    to perform optimistic locking.
    """
    search_fields = ('param_code', 'param_label')
    list_display = ('param_code', 'param_label', 'param_description')
    form = ParameterForm

admin.site.register(Parameter, ParameterAdmin)
