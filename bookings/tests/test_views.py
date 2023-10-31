from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import resolve, reverse_lazy

from bookings.forms import BookingForm
from bookings.views import BookingCreateView
from cart.cart import Cart


class BookingCreateTests(TestCase):
    """
    Test suite that checks all functionalities of the booking endpoint.

    Remember veer anytime you try to access BookingCreate view you should have
    these two things
        - 1. A search query in session
        - 2. A product in cart
    """

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse_lazy("bookings:booking-create")
        cls.template_name = "bookings/booking_form.html"

    def test_booking_create_url_resolve_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, BookingCreateView.as_view().__name__)

    # GET
    def test_booking_create_view_page_works_via_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

        self.assertContains(response, "Checkout")
        self.assertNotContains(response, "Hi I should not be on this page")

        self.assertIn("cart", response.context)
        self.assertIsInstance(response.context["cart"], Cart)

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], BookingForm)

    def test_booking_page_redirects_to_home_if_cart_is_empty(self):
        session = self.client.session
        session.clear()
        session.save()

        # Now try to access the booking page directly
        response = self.client.get(self.url)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("pages:home"), HTTPStatus.FOUND)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), BookingCreateView.redirect_message)
