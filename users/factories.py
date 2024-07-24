import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import factory

from properties.models import Addon, Property, Room

logger = logging.getLogger(__name__)


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


class PropertyOwnerFactory(UserFactory):
    """
    A normal user in our db who is also a property owner which basically
    means that he/she is added to the OwnerGroup.

    They have permissions to do CRUD only on their own property.
    """

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        logger.info("create:%s extracted:%s kwargs:%s" % (create, extracted, kwargs))
        # By default add this user to the Owner group.
        owners = OwnerGroupFactory()
        self.groups.add(owners)

        if not create or not extracted:
            # Simple build, or nothing to add so do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.groups.add(*extracted)


class GroupFactory(factory.django.DjangoModelFactory):
    """Generic factory to create groups in a sequence"""

    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "Group_{0}".format(n))


class OwnerGroupFactory(GroupFactory):
    """
    A group which represents owners of properties and has permissions to perform CRUD
    on Property and related models.
    """

    name = "Owners"

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        """
        Add CRUD permission to this group.
        """

        logger.info("create:%s extracted:%s kwargs:%s" % (create, extracted, kwargs))

        content_types = ContentType.objects.get_for_models(Property, Room, Addon)
        perms = Permission.objects.filter(content_type__in=content_types.values())

        self.permissions.add(*perms)

        if not create or not extracted:
            # Simple build, or nothing to add so do nothing
            return

        # Add the iterable of groups using bulk addition
        self.permissions.add(*extracted)
