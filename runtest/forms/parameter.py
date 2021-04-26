# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation

# Our modules
from runtest.models import Parameter
from runtest.models.record_owner import RECORD_OWNER_FIELDS
from .version_model_form import VersionModelForm

class ParameterForm(VersionModelForm):
    """
    This model has a last_version field, which we use to implement optimistic locking. We inherit 
    from this class for its clean_last_version method.
    """

    class Meta:
        model = Parameter
        exclude = RECORD_OWNER_FIELDS
