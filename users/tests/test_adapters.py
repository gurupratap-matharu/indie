from django.conf import settings
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy

from properties.factories import PropertyFactory
from users.adapter import MyAccountAdapter
from users.factories import (
    PropertyOwnerFactory,
    StaffuserFactory,
    SuperuserFactory,
    UserFactory,
)


class AdapterTests(TestCase):
    """
    Test suite for our custom allauth adapter
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner = PropertyOwnerFactory()
        cls.super_user = SuperuserFactory()
        cls.staff_user = StaffuserFactory()
        cls.user = UserFactory()

        cls.property = PropertyFactory(owner=cls.owner)
        cls.url = reverse_lazy("account_login")
        cls.adapter = MyAccountAdapter()

    def test_property_owner_is_redirected_to_respective_portal(self):
        # Create a django request with company owner
        request = RequestFactory().get(self.url)
        request.user = self.owner

        # Get login url from adapter for this request
        actual_url = self.adapter.get_login_redirect_url(request=request)

        # It should be equal to the company admin url
        expected_url = self.company.get_admin_url()

        self.assertEqual(actual_url, expected_url)

    def test_normal_user_is_redirected_to_default_login_url(self):
        for user in [self.super_user, self.staff_user, self.user]:
            request = RequestFactory().get(self.url)
            request.user = user

            # Get login url from adapter for this request
            redirect_url = self.adapter.get_login_redirect_url(request=request)

            self.assertEqual(redirect_url, settings.LOGIN_REDIRECT_URL)
