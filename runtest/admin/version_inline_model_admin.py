# From django
from django.contrib.admin.options import InlineModelAdmin

# Our modules
from runtest.models.version_field import FormVersionField

class VersionInlineModelAdmin(InlineModelAdmin):
    """
        This Inline Model Admin does exactly same things as VersionModelAdmin.
        But should be inheriting either Stacked or Tabular classes below, not
        this class.
    """
    def __init__(self, *args, **kwargs):

        if self.form:
            # This form MUST have our last_version field, otherwise should not be
            # inheriting from our class.
            if 'last_version' in self.form.base_fields:
                # fieldsets defined... 
                if getattr(self, 'fieldsets', None):
                    # fieldsets has one or more tuples of fieldset
                    # each fieldset is a tuple too, with the first element
                    # being the description (display as heading) and 
                    # second element is a dictionaries of tuples. There will
                    # be a dictionary key of 'fields' whose tuple we need to
                    # insert the last_version field.
                    # a fieldsets looks like this :-
                    # fieldsets = (
                    #               ('Fieldset description',                # fieldset 1
                    #                    {'fields' : (('field1', 'field2'), ('field3',)), # this fieldset has 2 tuples of fields
                    #                     'classes': ('collapse',)
                    #                    }
                    #               )
                    #               (),  # fieldset 2 and so on
                    #             )

                    # Turn tuple of fields into a list first (because tuple is immutable, so we cannot append)
                    field_list = list(self.fieldsets[0][1]['fields'])
                    # then add our field
                    field_list.append(('last_version',))
                    # Replace the original tuple with ours
                    self.fieldsets[0][1]['fields'] = tuple(field_list)
                # fields defined simply as a tuple, eg ('field1', 'field2',...)
                elif getattr(self, 'fields', None):
                    # Turn fields into a list
                    field_list = list(self.fields)
                    # then add our field
                    field_list.append('last_version')
                    # replace the original tuple
                    self.fields = tuple(field_list)
                # else if both fieldsets and fields are not defined, then base_fields already has
                # our last_version. We need to move this field to the back, else will screw
                # up inline grid
                else:
                    # Use dict base_fields to create a new fields, with last_version at end
                    # But for inlines, this will push the delete checkbox a bit to the right
                    base_fields = self.form.base_fields
                    # remove the original last version field, which is in front
                    del base_fields['last_version']
                    # get a list of fields using the keys of this dict only
                    field_list = list(base_fields.keys())
                    # append our field to the end
                    field_list.append('last_version')
                    # create a new fields
                    self.fields = tuple(field_list)
                    
        # Call parent's init
        super().__init__(*args, **kwargs)

# Admin forms should inherit from either of following for Inlines
class VersionStackedInline(VersionInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'

class VersionTabularInline(VersionInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
