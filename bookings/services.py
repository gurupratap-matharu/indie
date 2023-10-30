import logging
from timeit import default_timer as timer

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from bookings.models import Booking

logger = logging.getLogger(__name__)
current_site = Site.objects.get_current()


def booking_created(booking_id):
    """
    Send an e-mail notification to the payer confirming the creation of the booking
    with an booking id.

    The booking at this phase is still unpaid and payment is yet to be done.
    """
    start = timer()

    booking = get_object_or_404(
        Booking.objects.prefetch_related("items"), id=booking_id
    )
    context = {"booking": booking}

    subject = "Your Invoice from Indie Cactus"
    message = (
        f"Thanks for your booking {booking.first_name},\n\n"
        f"Attached is your invoice.\n"
        f"Your booking ID is {booking.id}."
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.email],
    )

    # Attach html version as an alternative
    # html_message = render_to_string(
    #     template_name="orders/emails/compiled/invoice.html", context=context
    # )
    # email.attach_alternative(content=html_message, mimetype="text/html")

    # Send email
    logger.info("sending invoice email...")

    mail_sent = email.send(fail_silently=False)

    end = timer()
    logger.info("took %.2f seconds", (end - start))

    return mail_sent


def booking_confirmed(booking_id):
    """
    Send confirmation email to traveller when a booking is successfully confirmed via webhook.
    """

    start = timer()

    subject_path = "bookings/emails/booking_confirmed_subject.txt"
    body_path = "bookings/emails/booking_confirmed_message.txt"

    booking = get_object_or_404(
        Booking.objects.prefetch_related("items"), id=booking_id
    )
    context = {"booking": booking, "current_site": current_site}

    # Confirm the booking
    logger.info("confirming booking...")
    # booking.confirm(payment_id=payment_id)

    subject = render_to_string(subject_path).strip()
    body = render_to_string(body_path, context).strip()

    # Generate the Email object
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.BOOKING_EMAIL,
        to=[booking.email, settings.DEFAULT_TO_EMAIL],
    )

    # Attach html version as an alternative
    # html_message = render_to_string(
    #     template_name="orders/emails/compiled/ticket.html", context=context
    # )
    # email.attach_alternative(content=html_message, mimetype="text/html")

    # Send email
    logger.info("sending booking email...")
    mail_sent = email.send(fail_silently=False)

    end = timer()
    logger.info("took %.2f seconds", (end - start))

    return mail_sent
