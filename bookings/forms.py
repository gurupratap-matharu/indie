import logging

from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Booking

logger = logging.getLogger(__name__)


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.errors:
            attrs = self[field].field.widget.attrs
            attrs.setdefault("class", "")
            attrs["class"] += " is-invalid"

    class Meta:
        model = Booking
        fields = ("first_name", "last_name", "email", "whatsapp", "residence")

        widgets = {  # noqa
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name", "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last Name", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "form-control"}
            ),
            "whatsapp": forms.TextInput(
                attrs={"placeholder": "Whatsapp", "class": "form-control"}
            ),
            "residence": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_first_name(self):
        return self.cleaned_data["first_name"].title()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].title()

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def send_mail(self, booking_id):
        cd = self.cleaned_data
        subject = f"Booking nr. {booking_id}"
        message = (
            f"Dear {cd['first_name']},\n\n"
            f"You booking is confirmed."
            f"Your Booking ID is {booking_id}."
        )

        logger.info("sending booking email...")
        
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[cd["email"], settings.DEFAULT_TO_EMAIL],
            fail_silently=False,
        )
