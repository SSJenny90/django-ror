from django import forms
from .models import Organization
from .widgets import RORSelect2Widget
import json
import jsonschema
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField, BS5Accordion
from crispy_forms.layout import Layout, Field, ButtonHolder, Row, Column, Button, Div
from crispy_forms.bootstrap import AccordionGroup
import requests
from django.utils.translation import gettext as _


class ModelGetOrCreateField(forms.ModelMultipleChoiceField):

    def prepare_value(self, value):
        if value is None:
            return value
        value = super().prepare_value(value)
        key = self.to_field_name or "pk"
        for v in value:
            self.queryset.get_or_create(**{key: v})
        return super().prepare_value(value)


class ResearchOrganisationForm(forms.ModelForm):
    # the field with which to query the ROR database
    institution = forms.CharField(widget=RORSelect2Widget)

    # a hidden field for storing the results returned from ROR
    info = forms.JSONField(widget=forms.HiddenInput)

    class Meta:
        model = Organization
        exclude = ['users', 'slug', 'geom', 'domains']

    def full_clean(self):
        if self.data:
            # self.data is a querydict and is therefore immutable
            # convert to a regular dict so we can add stuff
            self.data = dict(self.data)

            # for whatever reason this is return as a 1 length array
            # which throws an error, retrieve the first item which is
            # a json string
            ROR = json.loads(self.data['info'][0])

            for field in ['_resultId', 'disabled',
                          'element', 'selected', 'text']:
                # these fields are added by select2 but will not be accepted when
                # validating against the jsonschema from ROR
                del ROR[field]

            self.data['info'] = json.dumps(ROR)

            # update the original data dict with result from the json array
            # which contains data from ROR
            self.data.update(ROR)

        return super().full_clean()

    def clean_name(self):
        """Validate the incoming json structure agains the official ROR
        json schema (https://github.com/ror-community/ror-schema).

        .. note:

        We are validating in the 'name' field because the 'json' field is
        hidden and therefore feedback would not be visible to the user.

        Raises:
            ValidationError
        """
        data = json.loads(self.data['info'])

        # retrieve the current ROR schema which is stored locally in the
        # static folder
        with open(os.path.join(settings.STATIC_ROOT, 'ror/schema/ror_schema.json')) as f:
            schema = json.load(f)

        # validate against current ROR schema
        try:
            jsonschema.validate(data, schema)
        except Exception as e:
            raise ValidationError(
                'Validation against the ROR json schema failed with the following message:\n\n{}'.format(
                    e.message))

        return self.cleaned_data['name']


class ResearchOrganizationHTMX(forms.Form):
    id = forms.CharField(
        label=_('Organisation'),
        widget=RORSelect2Widget(
            attrs={
                'data-theme': 'bootstrap-5', }))

    class Meta:
        fields = ['id',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.include_media = False
        self.helper.attrs = {
            'hx-post': '',
            'hx-trigger': 'change',
            'hx-target': '#affiliationList',
            'hx-swap': "beforeend",
        }

    def fetch(self, id):
        response = requests.get(f"https://api.ror.org/organizations/{id}")
        return response.json()

    def clean_id(self):
        id = self.cleaned_data['id']
        data = self.fetch(id)

        with open(os.path.join(settings.STATIC_ROOT, 'ror/schema/ror_schema.json')) as f:
            schema = json.load(f)

        # validate against current ROR schema
        try:
            jsonschema.validate(data, schema)
        except Exception as e:
            raise ValidationError(
                'Validation against the ROR json schema failed with the following message:\n\n{}'.format(
                    e.message))
        self.cleaned_data['info'] = data
        return self.cleaned_data['id']
