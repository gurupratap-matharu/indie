import logging
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

logger = logging.getLogger(__name__)


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    email = models.EmailField(
        _("Email"), help_text=_("We'll email the reservation to this email id.")
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    whatsapp = models.CharField(_("Whatsapp"), validators=[phone_regex], max_length=17)
    residence = CountryField(
        _("Residence"),
        blank_label="(Country of residence)",
        help_text=_("This helps us to show you the best payment options."),
    )

    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=250, blank=True)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ("-created",)
        indexes = (models.Index(fields=["-created"]),)

    def __str__(self):
        return f"Booking {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class BookingItem(models.Model):
    booking = models.ForeignKey(
        "Booking", related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "properties.Room",
        related_name="booking_items",
        on_delete=models.SET_NULL,
        null=True,
    )
    price = models.DecimalField(_("Price"), max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        verbose_name = "Booking Item"
        verbose_name_plural = "Booking Items"

    def __str__(self):
        return f"Booking Item {self.id}"

    def get_cost(self):
        return self.price * self.quantity
