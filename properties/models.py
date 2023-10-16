import logging
import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

logger = logging.getLogger(__name__)


class Property(models.Model):
    HOSTEL = "HS"
    HOTEL = "HO"
    BB = "BB"
    CAMPSITE = "CS"
    APARTMENT = "AP"

    PROPERTY_TYPE_CHOICES = [
        (HOSTEL, "Hostel"),
        (HOTEL, "Hotel"),
        (BB, "Bed & Breakfast"),
        (CAMPSITE, "Campsite"),
        (APARTMENT, "Apartment"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="properties_created",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    description = models.TextField(_("description"), blank=True)

    property_type = models.CharField(
        _("Property Type"), max_length=10, choices=PROPERTY_TYPE_CHOICES
    )

    website = models.URLField(_("website"), blank=True)

    address_line1 = models.CharField(_("Address line 1"), max_length=128, blank=True)
    address_line2 = models.CharField(_("Address line 2"), max_length=128, blank=True)
    city = models.CharField(_("City"), max_length=64, blank=True)
    state = models.CharField(_("State/Province"), max_length=40, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=10)
    country = CountryField(blank_label=_("(select country)"))

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(_("phone"), validators=[phone_regex], max_length=17)
    email = models.EmailField(_("email"))

    latitude = models.DecimalField(_("Latitude"), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_("Longitude"), max_digits=9, decimal_places=6)

    legal_entity = models.CharField(_("Legal Entity"), max_length=200, blank=True)
    tax_id = models.CharField(_("Tax ID"), max_length=200, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "property"
        verbose_name_plural = "properties"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            logger.info("slugifying %s:%s..." % (self.name, slugify(self.name)))
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse_lazy("properties:property_detail", kwargs={"slug": self.slug})
