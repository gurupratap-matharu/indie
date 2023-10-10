from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Public app users with normal privileges"""

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda obj: "%s-%s" % (obj.first_name.lower(), obj.last_name.lower())
    )
    email = factory.LazyAttribute(lambda obj: "%s@email.com" % (obj.username))
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    location = factory.Faker("address")
    bio = factory.Faker("job")
    personal_website = factory.Faker("url")


class StaffuserFactory(UserFactory):
    """Internal users to Indie with staff privileges"""

    is_staff = True
    username = factory.Sequence(lambda n: "staffuser%d" % n)


class SuperuserFactory(StaffuserFactory):
    """This is me."""

    is_superuser = True
    username = factory.Sequence(lambda n: "superuser%d" % n)


class GroupFactory(factory.django.DjangoModelFactory):
    """Generic factory to create groups in a sequence"""

    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "Group_{0}".format(n))
