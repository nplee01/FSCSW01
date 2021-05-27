# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.contrib import admin

# Our modules
from runtest.models import TestRun
from .version_model_admin import VersionModelAdmin
from runtest.forms.test_run import TestRunForm

class TestRunAdmin(VersionModelAdmin):
    """
    We inherit from this class so that it will automatically insert the last version field
    to perform optimistic locking.
    # """

    # ASK: Do we need this v
    # search_fields = ('param_code', 'param_label')
    # list_display = ('param_code', 'param_label', 'param_description')
    form = TestRunForm

admin.site.register(TestRun, TestRunAdmin)

# from runtest.models import test_run
# admin.site.register(test_run.TestRun)