# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.contrib import admin

# Our modules
from runtest.models import test_run

admin.site.register(test_run.TestRun)