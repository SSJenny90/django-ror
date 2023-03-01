from django.contrib.gis.geos import Point
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _
from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationInvitation,
    AbstractOrganizationOwner,
    AbstractOrganizationUser,
)
from tldextract import extract


class RegisteredDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    domain = models.CharField(max_length=255)
    suffix = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        domain = extract(self.name)
        self.name = domain.registered_domain
        self.domain = domain.domain
        self.suffix = domain.suffix
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Organization(AbstractOrganization):
    """Core research organization model that mimics the ROR
    database structure"""

    ror = models.URLField(
        "id",
        validators=[RegexValidator("^https://ror.org/0[a-z|0-9]{8}$")],
        help_text=_(
            "Unique ROR ID for the organization. Stored as the url representation"
        ),
        null=True,
        blank=True,
    )
    extra = models.JSONField(
        _("ROR data"),
        default=dict,
        help_text=_("organizational information obtained from ROR"),
    )
    domains = models.ManyToManyField(
        RegisteredDomain,
        verbose_name=_("domains"),
        help_text=_("Registered domains sourced from the links field"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def save(self, *args, **kwargs):

        # create the organization slug if it doesn't exist already
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.info["name"]

        obj = super().save(*args, **kwargs)

        # convert links to RegisteredDomain objects and save to instance.
        # This must be done after saving the object if it is newly created
        domains = []
        for url in self.info["links"]:
            dom = RegisteredDomain.objects.get_or_create(
                name=extract(url).registered_domain
            )[0]
            domains.append(dom)

        self.domains.add(*domains)

        return obj

    def get(self, lookup):
        """Convenience function for accessing ROR data"""
        data = self.info
        for x in lookup.split("__"):
            data = data.get(x)
        return data

    def established(self):
        return self.get("established")

    established.admin_order_field = "info__established"
    established.short_description = _("established")

    def country(self):
        return self.get("country__country_name")

    country.admin_order_field = "info__country__country_name"
    country.short_description = _("country")

    def city(self):
        return self.get("addresses")[0].get("city", "")

    city.admin_order_field = "info__addresses__city"
    city.short_description = _("city")

    @property
    def location(self):
        if self.addresses:
            return Point(self.lng, self.lat)

    @property
    def lat(self):
        if self.addresses:
            return self.addresses[0].get("lat", "")

    @property
    def lng(self):
        if self.addresses:
            return self.addresses[0].get("lng", "")


class OrganizationUser(AbstractOrganizationUser):
    """Links a user to the organization"""

    def __str__(self):
        return f"{self.user}"


class OrganizationOwner(AbstractOrganizationOwner):
    """Identifies ONE user, by OrganizationUser, to be the owner"""

    def __str__(self):
        return f"{self.organization_user}"


class OrganizationInvitation(AbstractOrganizationInvitation):
    """Stores invitations for adding users to organizations"""

    pass
