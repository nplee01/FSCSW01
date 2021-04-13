# From django
from django.contrib.admin import ModelAdmin
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.utils.encoding import force_text
from django.conf.urls import url
from django.core.exceptions import PermissionDenied

class VersionModelAdmin(ModelAdmin):
    """
        This subclass of ModelAdmin will secretly insert the last_version field
        into the admin form, so that optimistic locking can be performed.
        Works together with VersionModelForm.

        A ModelAdmin form will display fields according to the following priority :-
        1) fieldsets
        2) fields
        3) base_fields (when 1 and 2 is not defined in ModelAdmin)

        So we shall insert our last_version into either fieldsets or fields.
        last_version should already be in base_fields of the form.

        We have also implemented Query views, as list and by object. These
        views reuses the change views but disables all fields and inlines.
    """
    # Make every child admin form place the Save buttons on top of page
    save_on_top = True
    # and also enable Duplicate Row function
    save_as = True
    # For displaying fieldsets or inlines as tabs. Inlines are named
    # lower(modelname)_set-group. Must make sure that this is passed 
    # into all templates used via extra_context. This is a tuple of tuples.
    # Each tuple is the tab name (using the fieldset name or inline name)
    # and the tooltip to be displayed.
    tabs_list = None

    def __init__(self, *args, **kwargs):
        if self.form:
            # This form MUST have our last_version field, otherwise should not be
            # inheriting from this class.
            if 'last_version' in self.form.base_fields:
                # fieldsets defined... 
                if getattr(self, 'fieldsets', None):
                    """
                    fieldsets has one or more tuples of fieldset
                    each fieldset is a tuple too, with the first element
                    being the description (display as heading) and 
                    second element is a dictionaries of tuples. There will
                    be a dictionary key of 'fields' whose tuple we need to
                    insert the last_version field.
                    a fieldsets looks like this :-
                    fieldsets = (
                                   ('Fieldset description',                # fieldset 1
                                        {'fields' : (('field1', 'field2'), ('field3',)), 
                                        # this fieldset has 2 tuples of fields
                                         'classes': ('collapse',)
                                        }
                                   )
                                   (),  # fieldset 2 and so on
                                 )

                    Turn tuple of fields into a list first (because tuple is immutable, 
                    so we cannot append)
                    """
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
                    field_list.append(('last_version',))
                    # replace the original tuple
                    self.fields = tuple(field_list)
                # else if both fieldsets and fields are not defined, then base_fields already has
                # our last_version. We need to move this field to the back, so that any error message
                # will come out at the end
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

    def has_query_permission(self, request):
        """
        Returns True if the given request has permission to query an object.
        Can be overriden by the user in subclasses.
        These are custom permissions that we added for this query view.
        These permissions are auto-created in infra/fixtures/group.py.
        """
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.query_' + opts.object_name.lower())

    def get_urls(self):
        """
        Add our own custom URLs.
        """
        urls = super(VersionModelAdmin, self).get_urls()
        # Add our own URLs to admin
        our_urls = [
            # Query List View
            url(r'^query/$', self.admin_site.admin_view(self.querylist_view)),
            # Query Object View
            url(r'^query/(?P<object_id>\d+)/$', self.admin_site.admin_view(self.query_object_view)),
        ]
        return our_urls + urls

    def allow_permission(self, request, obj=None):
        # To override permissions
        return True

    def deny_permission(self, request, obj=None):
        # To override permissions
        return False

    def querylist_view(self, request, extra_context=None):
        """
        Query List View. 

        We modified change_list template to accept a 
        query_only flag and temporarily grant change
        permissions to the model instance 
        (otherwise we cannot use changelist_view).
        """
        # Raise Exception when no query permission
        if not self.has_query_permission(request):
            raise PermissionDenied
        # We need to temporarily grant change permission to
        # the Object and its inlines because we are reusing
        # change_view. After calling change_view we restore
        # back the original permission functions.
        change_perm_func = self.has_change_permission
        delete_perm_func = self.has_delete_permission
        add_perm_func = self.has_add_permission
        actions = self.actions
        self.actions = None
        # We pass a query_only flag so that template can remove
        # change items (ie the form becomes query mode).
        extra_context = extra_context or {}
        extra_context['query_only'] = True
        extra_context['title'] = _("Query ") + force_text(self.model._meta.verbose_name_plural)
        setattr(self, 'has_change_permission', self.allow_permission)
        setattr(self, 'has_delete_permission', self.deny_permission)
        setattr(self, 'has_add_permission', self.deny_permission)
        clf = super(VersionModelAdmin, self).changelist_view(request, extra_context=extra_context)
        # Reset back to original function
        setattr(self, 'has_change_permission', change_perm_func)
        setattr(self, 'has_delete_permission', delete_perm_func)
        setattr(self, 'has_add_permission', add_perm_func)
        self.actions = actions
        return clf

    def query_object_view(self, request, object_id, extra_context=None):
        """
        Override change form to query specific object only.

        We reuse change_view by temporarily granting change
        permissions to the object and its inlines.
        """
        # Raise Exception when no query permission      
        if not self.has_query_permission(request):
            raise PermissionDenied
        # We need to temporarily grant change permission to
        # the Object and its inlines because we are reusing
        # change_view. After calling change_view we restore
        # back the original permission functions.
        change_perm_func = self.has_change_permission
        # We pass a query_only flag so that template can remove
        # change items (ie the form becomes query mode).
        extra_context = extra_context or {}
        extra_context['query_only'] = True
        extra_context['tabs_list'] = self.tabs_list
        extra_context['title'] = _("Query ") + force_text(self.model._meta.verbose_name)
        # Override permissions temporarily
        setattr(self, 'has_change_permission', self.allow_permission)
        # Do not have to deny add or delete because we disable the 
        # submit row in the template.
        # Inlines too need change permissions, else they won't display
        change_funcs = []
        delete_funcs = []
        add_funcs = []
        # Inline can change but take away add and delete
        for inline in self.inlines:
            change_funcs.append(inline.has_change_permission)
            delete_funcs.append(inline.has_delete_permission)
            add_funcs.append(inline.has_add_permission)
            setattr(inline, 'has_change_permission', self.allow_permission)
            setattr(inline, 'has_delete_permission', self.deny_permission)
            setattr(inline, 'has_add_permission', self.deny_permission)
        # Call change view but do not return yet
        rcf = super().change_view(request, object_id, extra_context=extra_context)
        # Reset back to original function
        setattr(self, 'has_change_permission', change_perm_func)
        for i in range(len(self.inlines)):
            setattr(self.inlines[i], 'has_change_permission', change_funcs[i])
            setattr(self.inlines[i], 'has_delete_permission', delete_funcs[i])
            setattr(self.inlines[i], 'has_add_permission', add_funcs[i])
        # Return result of change view
        return rcf
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Let template know what are the tabs list
        extra_context['tabs_list'] = self.tabs_list
        return super().change_view(request, object_id, form_url=form_url, 
            extra_context=extra_context)
                            
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Let template know what are the tabs list
        extra_context['tabs_list'] = self.tabs_list
        return super().add_view(request, form_url=form_url, extra_context=extra_context)
