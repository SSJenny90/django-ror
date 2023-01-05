from ror import models
from .forms import ResearchOrganisationForm
from django.contrib import admin
from django.utils.translation import gettext as _


class OwnerInline(admin.StackedInline):
    raw_id_fields = ("organization_user",)
    model = models.OrganizationOwner


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):

    # inlines = [OwnerInline]
    search_fields = ["name"]
    list_display = [
        'name',
        'established',
        'city',
        'country',
        # 'status',
        'is_active',
        '_domains',
    ]
    fields = [
        'id',
        'info',
        'domains',
    ]
    list_filter = ["is_active"]

    class Media:
        css = {
            'all': ('ror/css/select2.css',)
        }
        js = (
            'ror/js/select2.min.js',
            'ror/js/json_pprint.js'
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('domains')

    def get_readonly_fields(self, request, obj):
        if obj:
            return self.fields
        return super().get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """Return different forms for object creation versus object editing"""
        if not obj:
            return ResearchOrganisationForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj:
            return ['name', "info"]
        return super().get_fields(request, obj=None)

    def _domains(self, obj):
        return ", ".join(str(x) for x in obj.domains.all())
    _domains.short_description = _('domains')
    # _domains.admin_order_field = 'affiliation'


@admin.register(models.OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "is_admin"]
    raw_id_fields = ("user", "organization")


@admin.register(models.OrganizationOwner)
class OrganizationOwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ("organization_user", "organization")


@admin.register(models.OrganizationInvitation)
class OrganizationInvitationAdmin(admin.ModelAdmin):
    pass
