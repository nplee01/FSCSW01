# From Django
from django.utils.translation import ugettext_lazy as _ # To mark strings for translations
from django.db import models

# Our modules
from .record_owner import RecordOwner

class Parameter(RecordOwner):
    """
    Parameter settings to be used by Value Set Members.
    Allows dynamic prompting of parameter values that
    changes based on Value Set Member selected.
    """

    # Each Parameter has a Unique Code
    param_code = models.CharField(verbose_name=_("Parameter Code"), max_length=30, unique=True)
    # Prompt Label to be displayed
    param_label = models.CharField(verbose_name=_("Prompt Label"), max_length=20)
    # and a helpful description
    param_description = models.CharField(verbose_name=_("Description"), max_length=60, null=True, blank=True,
        help_text=_("A helpful description of this parameter"))
    # Default value when init form
    default_value = models.IntegerField(verbose_name=_("Default"), null=True)
    # Min/Max value to validate input
    min_value = models.IntegerField(verbose_name=_("Minimum"), null=True)
    max_value = models.IntegerField(verbose_name=_("Maximum"), null=True)
    step_by = models.IntegerField(verbose_name=_("Increment By"), null=True)
    # Multiplier to apply to input, eg input is a %, so multiply by 0.01 after input
    mult_by = models.FloatField(verbose_name=_("Multiply by"), null=True)

    class Meta:
        db_table = 'parameter'

    def __str__(self):
        # we prefer to describe ourself using code then description
        return self.param_code
