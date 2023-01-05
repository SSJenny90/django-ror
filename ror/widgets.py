from django.forms.widgets import Select, TextInput
from django import forms


class RORSelect2Widget(Select):

    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            'class': 'select2',
            'style': "width:450px;"}
        if attrs:
            attrs.update(default_attrs)
        else:
            attrs = default_attrs
        super().__init__(attrs, choices)

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                "https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css",
            )
        }
        js = (
            'ror/js/select2.min.js',
            'ror/js/select2_init.js',
        )
