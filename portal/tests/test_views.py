from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from portal.views import CalendarView, DashboardView, ScheduleView
from properties.factories import PropertyFactory
from users.factories import PropertyOwnerFactory, UserFactory


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
        cls.login_url = reverse("account_login")

    def test_dashboard_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, DashboardView.as_view().__name__)

    def test_dashboard_page_is_not_accessible_by_anonymous_user(self):
        response = self.client.get(self.url)
        redirect_url = f"{self.login_url}?next={self.url}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_dashboard_page_is_not_accessible_by_public_user(self):
        user = UserFactory()
        self.client.force_login(user)  # type:ignore

        response = self.client.get(self.url)

        # Assert user is not staff | superuser and correctly authenticated
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Assert user is forbidden access
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_dashboard_page_is_accessible_by_property_owner(self):
        self.client.force_login(self.owner)

        response = self.client.get(self.url)

        # Check if the owner is correctly authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Check if the owner can see the page
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, self.property.name)
        self.assertContains(response, "Dashboard")
        self.assertNotContains(response, "Hi I should not be on this page.")
        self.assertEqual(response.context["property"], self.property)


class CalendarPageTests(TestCase):
    """
    Test suite for the calendar page
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.template_name = "portal/calendar.html"
        cls.owner = PropertyOwnerFactory()
        cls.property = PropertyFactory(owner=cls.owner)
        cls.url = reverse("portal:calendar", kwargs={"slug": cls.property.slug})
        cls.login_url = reverse("account_login")

    def test_calendar_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, CalendarView.as_view().__name__)

    def test_calendar_page_is_not_accessible_by_anonymous_user(self):
        response = self.client.get(self.url)
        redirect_url = f"{self.login_url}?next={self.url}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_calendar_page_is_not_accessible_by_public_user(self):
        user = UserFactory()
        self.client.force_login(user)  # type:ignore

        response = self.client.get(self.url)

        # Assert user is not staff | superuser and correctly authenticated
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Assert user is forbidden access
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_calendar_page_is_accessible_by_property_owner(self):
        """Check if the property owner can access the calendar page"""

        self.client.force_login(self.owner)

        response = self.client.get(self.url)

        # Check if the owner is correctly authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Check if the owner can see the page
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, self.property.name)
        self.assertContains(response, "Calendar")
        self.assertNotContains(response, "Hi I should not be on this page.")
        self.assertEqual(response.context["property"], self.property)


class SchedulePageTests(TestCase):
    """
    Test suite for the schedule page
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.template_name = "portal/schedule.html"
        cls.owner = PropertyOwnerFactory()
        cls.property = PropertyFactory(owner=cls.owner)
        cls.url = reverse("portal:schedule", kwargs={"slug": cls.property.slug})
        cls.login_url = reverse("account_login")

    def test_schedule_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, ScheduleView.as_view().__name__)

    def test_schedule_page_is_not_accessible_by_anonymous_user(self):
        response = self.client.get(self.url)
        redirect_url = f"{self.login_url}?next={self.url}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_schedule_page_is_not_accessible_by_public_user(self):
        user = UserFactory()
        self.client.force_login(user)  # type:ignore

        response = self.client.get(self.url)

        # Assert user is not staff | superuser and correctly authenticated
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Assert user is forbidden access
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_schedule_page_is_accessible_by_property_owner(self):
        self.client.force_login(self.owner)

        response = self.client.get(self.url)

        # Check if the owner is correctly authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Check if the owner can see the page
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, self.property.name)
        self.assertContains(response, "Schedule")
        self.assertNotContains(response, "Hi I should not be on this page.")
        self.assertEqual(response.context["property"], self.property)
