# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.contrib import admin

# Our modules
from runtest.models import ValueSet, ValueSetMember
from .version_model_admin import VersionModelAdmin
from .version_inline_model_admin import VersionTabularInline
from runtest.forms.value_set import ValueSetForm, ValueSetMemberForm

class ValueSetMemberInline(VersionTabularInline):
    """
    We inherit from this class so that it will automatically insert the last version field
    to perform optimistic locking.
    """
    model = ValueSetMember
    form = ValueSetMemberForm

class ValueSetAdmin(VersionModelAdmin):
    """
    We inherit from this class so that it will automatically insert the last version field
    to perform optimistic locking.
    """
    search_fields = ('value_set_code',)
    list_display = ('value_set_code', 'value_set_description')
    form = ValueSetForm
    inlines = [ValueSetMemberInline]
    # Display as Tabs. Inlines are named lower(modelname)_set-group
    tabs_list = ((_("Value Set"), _("Create or change your Value Set details")),
        ("valuesetmember_set-group", _("Maintain the Members of this Value Set")))

admin.site.register(ValueSet, ValueSetAdmin)
