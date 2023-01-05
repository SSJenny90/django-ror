from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ror'
    vebose_name = _('Research Organization')
    vebose_name_plural = _('Research Organizations')
