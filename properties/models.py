import logging
import uuid
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Min, Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from .managers import FutureManager

logger = logging.getLogger(__name__)


class HostelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(property_type="HS")


class Property(models.Model):
    HOSTEL = "HS"
    HOTEL = "HO"
    BB = "BB"
    CAMPSITE = "CS"
    APARTMENT = "AP"

    PROPERTY_TYPE_CHOICES = [  # noqa: RUF012
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
    # cover = models.ImageField(upload_to="properties/%Y/%m/%d", blank=True)
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

    active = models.BooleanField(_("Active"), default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    hostels = HostelManager()

    class Meta:
        ordering = ["-created"]  # noqa: RUF012
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            slug = slugify(self.name)
            logger.info("slugifying %s:%s" % (self.name, slug))
            self.slug = slug

        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse_lazy("properties:property-detail", kwargs={"slug": self.slug})

    def get_portal_url(self) -> str:
        return reverse_lazy("portal:dashboard", kwargs={"slug": self.slug})


class Room(models.Model):
    BASIC = "BA"
    STANDARD = "ST"
    DELUXE = "DL"
    SUPERIOR = "SP"

    GRADE_CHOICES = [  # noqa: RUF012
        (BASIC, "Basic"),
        (STANDARD, "Standard"),
        (DELUXE, "Deluxe"),
        (SUPERIOR, "Superior"),
    ]

    MIXED_DORM = "XD"
    MALE_DORM = "MD"
    FEMALE_DORM = "FD"
    PRIVATE_ROOM = "PR"
    DOUBLE_BED = "DB"
    APARTMENT = "AP"
    FAMILY_ROOM = "FR"
    PRIVATE_TENT = "PT"
    SHARED_TENT = "ST"

    ROOM_TYPE_CHOICES = [  # noqa: RUF012
        (MIXED_DORM, "Mixed Dorm"),
        (MALE_DORM, "Male Dorm"),
        (FEMALE_DORM, "Female Dorm"),
        (PRIVATE_ROOM, "Private Room"),
        (DOUBLE_BED, "Double Bed"),
        (APARTMENT, "Apartment"),
        (FAMILY_ROOM, "Family Room"),
        (PRIVATE_TENT, "Private Tent"),
        (SHARED_TENT, "Shared Tent"),
    ]

    property = models.ForeignKey(
        "properties.Property", related_name="rooms", on_delete=models.CASCADE
    )
    name = models.CharField(_("Name"), blank=True, max_length=64)
    # cover = models.ImageField(upload_to="rooms/%Y/%m/%d", blank=True)
    grade = models.CharField(
        _("Grade"), max_length=3, choices=GRADE_CHOICES, default=STANDARD
    )
    num_of_guests = models.PositiveSmallIntegerField(
        _("Number of Guests"), validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    room_type = models.CharField(
        _("Room Type"), max_length=3, choices=ROOM_TYPE_CHOICES, default=PRIVATE_ROOM
    )
    ensuite = models.BooleanField(
        verbose_name=_("Ensuite"),
        help_text=_("Does it have attached bathroom?"),
        default=True,
    )
    description = models.TextField(_("Description"), blank=True)
    weekday_price = models.DecimalField(
        _("Weekday Price"),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    weekend_price = models.DecimalField(
        _("Weekend Price"),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    active = models.BooleanField(_("Active"), default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ("property", "room_type")

    def __str__(self):
        return f"{self.name}"

    def get_add_to_cart_url(self):
        return reverse_lazy("cart:cart-add", kwargs={"product_id": self.id})

    def get_schedule_url(self):
        return reverse_lazy(
            "portal:schedule-detail",
            kwargs={"slug": self.property.slug, "room_id": self.id},
        )

    def get_cost(self, start, end) -> Decimal:
        """
        Find the total cost of a room within specified dates.
        """

        if end < start:
            error_msg = "End date:%(end)s cannot be less than Start date:%(start)s"
            raise ValidationError(
                error_msg,
                params={"start": start, "end": end},
                code="invalid",
            )

        qs = self.occurrences.filter(for_date__range=(start, end))
        cost = qs.aggregate(total=Sum("rate")).get("total", 0)
        cost = cost or Decimal(0)
        logger.info("Room:%s, from:%s till:%s Cost:$%s" % (self, start, end, cost))

        return cost

    def get_availability(self, start, end) -> int:
        """
        Calculate the min availability over a date range

        For shared rooms like dorms if availability today=3, tomorrow=4, day_after=5 -> return 3
        For private rooms availability is either 1 (available) or 0 (not available)
        """

        if end < start:
            error_msg = "End date:%(end)s cannot be less than Start date:%(start)s"
            raise ValidationError(
                error_msg,
                params={"start": start, "end": end},
                code="invalid",
            )

        qs = self.occurrences.filter(for_date__range=(start, end))
        availability = qs.aggregate(available=Min("availability")).get("available", 0)

        availability = availability or 0

        logger.info(
            "Room:%s, from:%s till:%s Availability:%s"
            % (self, start, end, availability)
        )

        return availability

    def is_dorm(self):
        return self.room_type in {self.MIXED_DORM, self.FEMALE_DORM, self.MALE_DORM}

    def is_private(self):
        return not self.is_dorm()


class Occurrence(models.Model):
    """
    Holds the rates and availability data for each room across each day.
    """

    rate = models.DecimalField(
        _("Rate"), max_digits=12, decimal_places=2, validators=[MinValueValidator(1)]
    )
    availability = models.PositiveIntegerField(
        _("Availability"), default=1, validators=[MaxValueValidator(20)]
    )
    room = models.ForeignKey(
        "Room",
        verbose_name=_("Room"),
        on_delete=models.CASCADE,
        related_name="occurrences",
    )
    for_date = models.DateField(
        _("For Date"),
        help_text=_("The date for the night the guest will stay at the property"),
        validators=[MinValueValidator(limit_value=timezone.localdate)],
    )

    objects = models.Manager()
    future = FutureManager()

    class Meta:
        verbose_name = _("Occurrence")
        verbose_name_plural = _("Occurrences")
        ordering = ("for_date",)

        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["room", "for_date"], name="unique_occurrence"
            ),
        ]

    def __str__(self):
        return f"Occ: {self.for_date}"

    def __lt__(self, other):
        return self.for_date < other.for_date


class Addon(models.Model):
    """
    An additional item that a property can bill to a traveller.
    """

    property = models.ForeignKey(
        "properties.Property", related_name="addons", on_delete=models.CASCADE
    )

    name = models.CharField(_("name"), max_length=64)
    price = models.DecimalField(
        _("Price"), max_digits=12, decimal_places=2, validators=[MinValueValidator(1)]
    )
    icon = models.CharField(_("icon"), max_length=64, blank=True)
    active = models.BooleanField(_("active"), default=True)

    class Meta:
        verbose_name = "Addon"
        verbose_name_plural = "Addons"
        ordering = ("name",)
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["property", "name"], name="unique_addon"),
        ]

    def __str__(self):
        return f"{self.name}: {self.price}"
