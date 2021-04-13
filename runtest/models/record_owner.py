# From Django
from django.utils.translation import ugettext_lazy as _ # To mark strings for translations
from django.db import models
from django.utils import timezone

# Our own modules
from runtest.threadlocals import get_current_user
from .version_field import VersionField

# List of Record Owner fields (except last_version which must be included in all forms)
RECORD_OWNER_FIELDS = ['created_by', 'created_on', 'updated_by', 'updated_on']

class RecordOwner(models.Model): 
    """
    We implement our own abstract models that has the
    standard Record Owner fields and last updated version field.
    """

    # Standard fields which cannot be edited, username follows length in auth_user
    created_by = models.CharField(verbose_name=_("Created By"), max_length=150, editable=False,
        null=True, blank=True, help_text=_("This row was created by this User"))
    created_on = models.DateTimeField(verbose_name=_("Created On"), editable=False, blank=True, null=True, 
        help_text=_("Created on this date and time"))
    updated_by = models.CharField(verbose_name=_("Updated By"), max_length=150, editable=False,
        null=True, blank=True, help_text=_("This row was last updated by this User"))
    updated_on = models.DateTimeField(verbose_name=_("Updated On"), editable=False, blank=True, null=True, 
        help_text=_("Last updated on this date and time"))
    # Last Version is incremented whenever row is updated. Forms using any Record Owner models must
    # make a check between queried last version and the value in the table at the time of saving or deleting.
    # Cannot implement here because no access to the queried last_version at the start of a transaction.
    # We make it a hidden field in all Forms so that its value is available in forms clean and save_instance methods
    last_version = VersionField(default=0, blank=True, null=True)

    class Meta:
        # This model is abstract, ie will never have its own DB table
        abstract = True

    # Override save method to capture User who created or updated row
    # Most people would say the 'right' place for this code
    # is in ModelAdmin's save_model() but some of our objects are
    # created not in admin but in batch postings. So the anomaly here
    # is that instead of request.user, we are using threadlocals where
    # we stashed our login user.
    def save(self, force_insert=False, force_update=False):
        # Get current user
        user = get_current_user()
        if user:
            username = user.username if user.is_authenticated else 'visitor'
            # We want the username only, not the object
            if getattr(self, 'created_by', None) is None:
                # Set the creator user the first time only
                self.created_by = username
                self.created_on = timezone.now()
                self.last_version = 0
            else:
                # The next time are updates 
                self.updated_by = username
                self.updated_on = timezone.now()
                # Increment last version
                self.last_version = (self.last_version or 0) + 1

        # Perform the actual save
        super().save(force_insert, force_update)
