# From django
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.utils import ErrorList
from django.db import models

# Our modules
from runtest.models.version_field import FormVersionField

class VersionModelForm(ModelForm):
    """
    All our admin forms will use this ModelForm so that optimistic locking is implemented on update.
    We use the last_version field to implement this. It is hidden in the Admin Form, either in the fieldsets or
    field when either is defined.
    """

    # Admin does not honour our field's widget which has the hidden attribute,
    # so we must define it here again
    last_version = FormVersionField()

    def clean_last_version(self):
        "Override clean method to check for model instance in database if changed"

        # Our last version field must be a hidden field (as defined by our custom VersionField
        last_version = self.cleaned_data['last_version']
        # instance is the model's row from db and check only for updates
        # new row's pk is none
        if self.instance.pk and self.instance.last_version != last_version:
            print('Last Version in form %d vs Instance %d' % (last_version, self.instance.last_version))
            error_message = (_("This row has been changed by %(username)s. Please requery and retry update.") %
                    {'username': self.instance.updated_by})
            # We make this an error for the whole form, in case last_version completely hidden (by inline forms)
            self._errors['__all__'] = ErrorList([error_message])
            # when a field is invalid, remove it from cleaned_data (because it is unclean)
            del self.cleaned_data['last_version']
            raise ValidationError(error_message, code='last_version')

        # no exception raised, then return field as is, this means no validation error
        return last_version
