from django.test import TestCase
from django.urls import resolve, reverse

from portal.views import DashboardView
from properties.factories import PropertyFactory
from users.factories import PropertyOwnerFactory


class DashboardPageTests(TestCase):
    """
    Test suite for the portal main dashboard page.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.template_name = "portal/dashboard.html"
        cls.owner = PropertyOwnerFactory()
        cls.property = PropertyFactory(owner=cls.owner)
        cls.url = reverse("portal:dashboard", kwargs={"slug": cls.property.slug})

    def test_dashboard_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, DashboardView.as_view().__name__)
