from http import HTTPStatus

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse_lazy

from payments.views import (
    PaymentFailView,
    PaymentPendingView,
    PaymentSuccessView,
    PaymentView,
    mercadopago_success,
)


class PaymentHomeTests(TestCase):
    """
    Test suite for payments home page view which shows all payments options like
    Stripe, MercadoPago, etc.
    """

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse_lazy("payments:home")
        cls.template_name = "payments/home.html"

    def test_payment_home_page_url_resolve_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, PaymentView.as_view().__name__)


class MercadoPagoSuccessTests(SimpleTestCase):
    """
    Test suite for custom MP success view which parses GET parameters
    and confirms a booking.
    We recall that this view simply parses the URL and executes some logic and then redirects
    to the final PaymentSuccessView. It does not render a template.
    """

    def setUp(self):
        self.url = reverse_lazy("payments:mercadopago-success")

    def test_mercadopago_success_view_redirects_correctly(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response, reverse_lazy("payments:success"), HTTPStatus.FOUND
        )

    def test_mercado_pago_success_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, mercadopago_success.__name__)

    def test_mercado_pago_success_views_confirms_booking_with_correct_query_params(
        self,
    ):
        self.fail()

    def test_mercado_pago_success_view_does_not_confirms_booking_with_incorrect_query_params(
        self,
    ):
        self.fail()


class PaymentSuccessTests(SimpleTestCase):
    """Test suite for payment success view"""

    def setUp(self):
        self.url = reverse_lazy("payments:success")
        self.template_name = "payments/payment_success.html"

    def test_payment_success_page_works(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, "Success")
        self.assertContains(response, "Your booking is confirmed")
        self.assertNotContains(response, "Hi I should not be on this page")

    def test_payment_success_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, PaymentSuccessView.as_view().__name__)


class PaymentPendingTests(SimpleTestCase):
    """Test suite for payment pending view"""

    def setUp(self):
        self.url = reverse_lazy("payments:pending")
        self.template_name = "payments/payment_pending.html"

    def test_payment_pending_page_works(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, "Payment Pending")
        self.assertContains(
            response,
            "We were unable to receive a confirmation for your payment and looks like its in pending status.",
        )
        self.assertNotContains(response, "Hi I should not be on this page")

    def test_payment_pending_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, PaymentPendingView.as_view().__name__)


class PaymentFailTests(SimpleTestCase):
    """Test suite for payment failed view"""

    def setUp(self):
        self.url = reverse_lazy("payments:fail")
        self.template_name = "payments/payment_fail.html"

    def test_payment_fail_page_works(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, "Payment Unsuccessful")
        self.assertContains(
            response, "We were unable to receive a confirmation for your payment."
        )
        self.assertNotContains(response, "Hi I should not be on this page")

    def test_payment_fail_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, PaymentFailView.as_view().__name__)
