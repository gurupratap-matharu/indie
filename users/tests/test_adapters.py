from django.test import TestCase
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
        pass

    def test_normal_user_is_redirected_to_default_login_url(self):
        pass
