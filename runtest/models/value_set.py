# From Django
from django.utils.translation import ugettext_lazy as _ # To mark strings for translations
from django.db import models

# Our modules
from .record_owner import RecordOwner
from .parameter import Parameter

class ValueSet(RecordOwner):
    """
    Application specific List of Values.

    A value set is a List of Values used in this application. 
    Instead of hardcoding these lists, we create a set of values 
    here. Each ValueSet has as children one or more ValueSetMembers
    whose Value Code and Description are used to
    build the drop-down list (for the HTML Select Input).
    Use the class method get_choices() for this.

    Whenever you want to create a model that has just a Code and
    a Value, avoid doing so and just create a new ValueSet. Use
    your model name (in uppercase) as the Value Set Code. In
    addition, we allow up to 3 params per Value, which your
    own program can use in anyway it likes.
    """
    # Each Value Set has a Unique Code
    value_set_code = models.CharField(verbose_name=_("Value Set Code"), max_length=30, unique=True)
    # and a helpful description
    value_set_description = models.CharField(verbose_name=_("Description"), max_length=60, null=True, blank=True,
        help_text=_("A helpful description of this Value Set"))

    class Meta:
        db_table = 'value_set'

    def __str__(self):
        # we prefer to describe ourself using code then description
        return self.value_set_code

    def get_choices(self, is_required=False):
        # Cannot use lazy translation as caller may need to serialize to send to frontend
        from django.utils.translation import ugettext as _ # To mark strings for translation
        choices = []
        if self.id:
            # For mandatory fields, should pass in is required True
            if not is_required:
                choices = [(u'', _("No Selection"))]
            # Must prepend an empty selection for Fields that allows blank=True
            choices += [(row.value_code, row.value_description)
                for row in self.valuesetmember_set.all().order_by('sort_order', 'value_code')]
        # Return a List of 2 value Tuples as choices
        return choices

class ValueSetMember(RecordOwner):
    """
    Children of a Value Set. 
    """
    # Parent Value Set
    value_set = models.ForeignKey(ValueSet, on_delete=models.PROTECT, verbose_name=_("Value Set"))
    # A unique Value Code
    value_code = models.CharField(verbose_name=_("Value Code"), max_length=30, 
        help_text=_("A Unique Value Code within this Value Set"))
    # with a helpful description
    value_description = models.CharField(verbose_name=_("Description"), max_length=60, null=True, blank=True,
        help_text=_("A helpful description of this Value Code"))
    sort_order = models.PositiveSmallIntegerField(verbose_name=_("Sort Order"), 
        blank=True, null=True,
        help_text=_("Optionally override sorting by Value Code"))
    # up to 3 optional Parameters that accept integers
    param_1 = models.ForeignKey(Parameter, on_delete=models.PROTECT, verbose_name=_("Parameter 1"),
            null=True, related_name='param_1')
    param_2 = models.ForeignKey(Parameter, on_delete=models.PROTECT, verbose_name=_("Parameter 2"),
            null=True, related_name='param_2')
    param_3 = models.ForeignKey(Parameter, on_delete=models.PROTECT, verbose_name=_("Parameter 3"),
            null=True, related_name='param_3')

    class Meta:
        db_table = 'value_set_member'

    def __str__(self):
        return self.value_code
