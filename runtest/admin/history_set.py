# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.contrib import admin

# Our modules
from runtest.models import history_set

admin.site.register(history_set.historySet)
