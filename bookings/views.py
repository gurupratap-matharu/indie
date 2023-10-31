import logging
from typing import Any

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from cart.cart import Cart

from .forms import BookingForm
from .models import BookingItem

logger = logging.getLogger(__name__)


class BookingCreateView(FormView):
    form_class = BookingForm
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy("payments:home")
    redirect_message = "Your session has expired. Please search again 🙏"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """
        If session or cart is empty then redirect user to home
        # TODO: check for search query in session
        """

        # q = request.session.get("q")
        cart = request.session.get("cart")

        if not cart:
            messages.info(request, self.redirect_message)
            return redirect("pages:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context

    def form_valid(self, form):
        logger.info("booking form is valid...")

        cart = Cart(self.request)
        booking = form.save()
        booking_id = str(booking.id)

        for item in cart:
            logger.info("creating BookingItem:{item}", extra={"item": item})

            _ = BookingItem.objects.create(
                booking=booking,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"],
            )

        cart.clear()

        form.send_mail(booking_id=booking_id)
        self.request.session["booking"] = booking_id

        return super().form_valid(form)
