from django.db import models
from django.forms import fields, widgets

class FormVersionField(fields.IntegerField):
    "Our Last Version field handles optimistic locking. We hide it in all Forms"
    widget = widgets.HiddenInput

    def __init__(self, *args, **kwargs):
        # This field is always hidden
        kwargs['label'] = u''
        kwargs['required'] = False
        self.widget.is_hidden = True  # in admin template, this becomes field.field.field.widget.is_hidden
        self.is_hidden = True         # in admin template, this becomes field.field.is_hidden
        # Allow parent to continue its init
        super().__init__(*args, **kwargs)

class VersionField(models.PositiveIntegerField):
    # Used only in models/record_owner
    def formfield(self, **kwargs):
        # To override form widget to hidden when creating forms
        defaults = {'form_class': FormVersionField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

