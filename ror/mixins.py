from django.contrib import admin
from django.utils.translation import gettext as _
# from django.contrib.sites import models


class ChangeListQuickAdd():
    """Django Admin mixin that adds a select2 input to the top of the
    list_view. Submission of the select2 box is via ajax to a user defined URL.
    """
    select2 = {}
    change_list_template = 'admin/crossref/quick_add.html'

    def changelist_view(self, request, extra_context={}):
        # extra_context['select2'] = self.select2
        # extra_context['select'] = self.get_model_fields()
        # extra_context['doi_form'] = DOIForm()
        # extra_context['bibtex_import_form'] = UploadForm()
        return super().changelist_view(request, extra_context)

    def get_model_fields(self):
        return [f.name.replace('_', '-')
                for f in self.model._meta.get_fields()]
