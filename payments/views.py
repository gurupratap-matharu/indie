import logging
from http import HTTPStatus
from typing import Any, Dict

from django.conf import settings
from django.contrib import messages
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

import mercadopago

from bookings.models import Booking
from bookings.services import booking_confirmed

logger = logging.getLogger(__name__)

mercado_pago = mercadopago.SDK(settings.MP_ACCESS_TOKEN)


class PaymentView(TemplateView):
    """A simple view that shows all payment options for our project"""

    template_name: str = "payments/home.html"
    booking = None
    redirect_message = "Your session has expired. Please search again 🙏"

    def dispatch(self, request, *args, **kwargs):
        """
        If no booking in session then redirect user to home.
        """

        booking = request.session.get("booking")

        if not booking:
            messages.info(request, self.redirect_message)
            return redirect("pages:home")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        booking_id = self.request.session.get("booking")

        context = super().get_context_data(**kwargs)

        context["booking"] = self.booking = get_object_or_404(Booking, id=booking_id)
        context["preference"] = self.get_mercado_pago_preference()
        context["mp_public_key"] = settings.MP_PUBLIC_KEY

        logger.info("veer retrieved booking(👩🏻‍⚖️) from session as: %s", self.booking)

        return context

    def get_mercado_pago_preference(self):
        """Get reponse from Mercado Pago for preference (item) data."""

        uri = self.request.build_absolute_uri
        booking = self.booking
        unit_price = float(
            booking.get_total_cost() / 1000
        )  # <-- Minimizing this for MP

        picture_url = uri(static("assets/logos/logo.png"))
        success = uri(reverse_lazy("payments:mercadopago-success"))
        failure = uri(reverse_lazy("payments:fail"))
        pending = uri(reverse_lazy("payments:pending"))
        notification_url = uri(reverse_lazy("payments:mercadopago-webhook"))

        logger.info("success: %s", success)
        logger.info("failure: %s", failure)
        logger.info("pending: %s", pending)
        logger.info("picture_url: %s", picture_url)
        logger.info("notification_url: %s", notification_url)
        logger.info("unit price: %s", unit_price)

        # Create mercado page preference
        # veer we use quantity as always 1 with full booking price 😉
        preference_data = {
            "items": [
                {
                    "id": str(booking.id),
                    "title": "Booking",  # <-- could be customized
                    "currency_id": "ARS",
                    "picture_url": picture_url,
                    "description": "Accomodation Booking",  # <-- could be customized
                    "category_id": "Accomodation",
                    "quantity": 1,
                    "unit_price": unit_price,
                }
            ],
            # "payer": {
            #     "name": booking.first_name,
            #     "surname": "",
            #     "email": booking.email,
            #     "phone": {"area_code": "11", "number": "4444-4444"},
            #     "identification": {"type": "DNI", "number": "12345678"},
            #     "address": {
            #         "street_name": "Uspallata",
            #         "street_number": 471,
            #         "zip_code": "1096",
            #     },
            # },
            "back_urls": {
                "success": success,
                "failure": failure,
                "pending": pending,
            },
            "payment_methods": {
                "excluded_payment_methods": [],
                "excluded_payment_types": [],
                "installments": 1,
            },
            "auto_return": "approved",
            "notification_url": notification_url,
            "statement_descriptor": "Indie Cactus 🌵",
            "external_reference": str(booking.id),
            "binary_mode": True,
        }

        preference = mercado_pago.preference().create(preference_data)
        logger.info("MP preference_data: %s", preference_data)
        logger.info("MP preference response(💰): %s", preference)

        return preference["response"]


class PaymentSuccessView(TemplateView):
    template_name: str = "payments/payment_success.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # We store the booking id in session to generate the reservation pdf if requested
        # before clearing the session as user might wish to do another booking
        context["booking_id"] = self.request.session.get("booking")

        # next since booking is confirmed we remove it from the session
        try:  # noqa
            del self.request.session["booking"]
        except KeyError:
            # TODO: technically here veer you should redirect as its not a valid case!
            pass

        return context


class PaymentPendingView(TemplateView):
    template_name: str = "payments/payment_pending.html"


class PaymentFailView(TemplateView):
    template_name: str = "payments/payment_fail.html"


@csrf_exempt
@require_POST
def mercadopago_webhook(request):
    """
    Our internal webhook to receive payment updates from mercado pago.

    A confirmation on this hook is a guarantee that the payment is successful.
    # TODO: May be store the confirmation data in a model or email
    """

    logger.info("mercadopago webhook request.GET(🤝):%s", request.GET)
    logger.info("mercadopago webhook request.POST(🤝):%s", request.POST)
    logger.info("mercadopago webhook request.body(🤝):%s", request.body)

    return HttpResponse(status=HTTPStatus.OK)


def mercadopago_success(request):
    """
    Parses the query parameters sent by mercado pago when a payment is succesful
    and routes to our PaymentSuccess endpoint. By itself this view does not render any template
    but is just an intermediate processing step.

    This is not a webhook of mercado pago. My understanding is that mercado pago is appending
    payment response as query params to the `success_url` via GET request.

    At the time of implementation I realise that it might not be safe to show mercado pago
    payment details right in the query parameters.

    An example of successful query params is like this...

    /payments/success/?collection_id=54650347595&collection_status=approved&payment_id=54650347595&status=approved&external_reference=7a231700-d000-47d0-848b-65ff914a9a3e&payment_type=account_money&merchant_order_id=7712864656&preference_id=1272408260-35ff1ef7-3eb8-4410-b219-4a98ef386ac0&site_id=MLA&processing_mode=aggregator&merchant_account_id=null
    """

    mercadopago_response = request.GET
    msg = "mercado pago says(🤝):%s" % mercadopago_response
    logger.info(msg) if mercadopago_response else logger.warning(msg)

    booking_id = mercadopago_response.get("external_reference")
    status = mercadopago_response.get("status")
    payment_id = mercadopago_response.get("payment_id")

    logger.info("booking_id:%s" % booking_id)
    logger.info("status: %s" % status)
    logger.info("payment_id:%s" % payment_id)

    if (status == "approved") and booking_id:
        logger.info("mercadopago(🤝) payment successful!!!")

        booking = get_object_or_404(Booking, id=booking_id)
        # Confirm the booking
        booking.confirm(payment_id=payment_id)

        # Send confirmation emails
        booking_confirmed(booking_id=booking_id)
        messages.success("Payment Successful 🎉")

        return redirect(reverse_lazy("payments:success"))

    # Need to check this. In case of payments pending or failure the webhook is still
    # triggered. We need to analyse the get parameteres
    logger.info("mercadopago(🤝) payment unsuccessful 🛑")

    # email the admins for troubleshooting
    mail_admins(subject="MercadoPago Payment Issue", message=msg)

    return redirect(reverse_lazy("payments:fail"))
