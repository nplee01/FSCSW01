# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation

# Our modules
from runtest.models import ValueSet, ValueSetMember
from runtest.models.record_owner import RECORD_OWNER_FIELDS
from .version_model_form import VersionModelForm

class ValueSetForm(VersionModelForm):
    """
    This model has a last_version field, which we use to implement optimistic locking. We inherit 
    from this class for its clean_last_version method.
    """

    class Meta:
        model = ValueSet
        exclude = RECORD_OWNER_FIELDS

class ValueSetMemberForm(VersionModelForm):
    """
    This model has a last_version field, which we use to implement optimistic locking. We inherit 
    from this class for its clean_last_version method.
    """

    class Meta:
        model = ValueSetMember
        exclude = RECORD_OWNER_FIELDS
