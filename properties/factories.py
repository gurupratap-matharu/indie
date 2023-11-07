from datetime import timedelta

from django.template.defaultfilters import slugify
from django.utils import timezone

import factory
from django_countries import countries
from factory import fuzzy

from users.factories import PropertyOwnerFactory

from .models import Addon, Occurrence, Property, Room
from .samples import ROOM_SAMPLES


class PropertyFactory(factory.django.DjangoModelFactory):
    """
    Factory to create demo properties in database.
    """

    class Meta:
        model = Property
        django_get_or_create = ("slug",)

    owner = factory.SubFactory(PropertyOwnerFactory)
    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = factory.Faker("paragraph")
    property_type = fuzzy.FuzzyChoice(
        Property.PROPERTY_TYPE_CHOICES, getter=lambda c: c[0]
    )
    website = factory.Faker("url")
    address_line1 = factory.Faker("address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    postal_code = factory.Faker("postalcode")
    country = factory.Faker("random_element", elements=list(dict(countries)))
    phone = factory.Sequence(lambda n: "+54261123%03d" % n)
    email = factory.Faker("company_email")

    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")

    legal_entity = factory.Faker("isbn13")
    tax_id = factory.Faker("isbn10")


class HostelFactory(PropertyFactory):
    property_type = Property.HOSTEL


class RoomFactory(factory.django.DjangoModelFactory):
    """
    Creates amazing room objects for any property
    """

    class Meta:
        model = Room

    property = factory.SubFactory(PropertyFactory)

    name = fuzzy.FuzzyChoice(list(ROOM_SAMPLES))
    # grade = fuzzy.FuzzyChoice(Room.GRADE_CHOICES, getter=lambda c: c[0])
    # num_of_guests = factory.Faker("random_int", min=1, max=20)
    # room_type = fuzzy.FuzzyChoice(Room.ROOM_TYPE_CHOICES, getter=lambda c: c[0])
    # weekday_price = factory.Faker("random_element", elements=[10, 25, 50, 100])
    # weekend_price = factory.LazyAttribute(lambda o: o.weekday_price * 1.2)
    grade = factory.LazyAttribute(lambda o: ROOM_SAMPLES[o.name]["grade"])
    num_of_guests = factory.LazyAttribute(
        lambda o: ROOM_SAMPLES[o.name]["num_of_guests"]
    )
    room_type = factory.LazyAttribute(lambda o: ROOM_SAMPLES[o.name]["room_type"])
    ensuite = factory.Faker("boolean")
    description = factory.LazyAttribute(lambda o: ROOM_SAMPLES[o.name]["description"])
    weekday_price = factory.LazyAttribute(
        lambda o: ROOM_SAMPLES[o.name]["weekday_price"]
    )
    weekend_price = factory.LazyAttribute(
        lambda o: ROOM_SAMPLES[o.name]["weekend_price"]
    )


class OccurrenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Occurrence
        django_get_or_create = ("room", "for_date")

    room = factory.SubFactory(RoomFactory)
    rate = factory.LazyAttribute(lambda o: o.room.weekday_price)
    availability = 1
    for_date = fuzzy.FuzzyDate(
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=90),
    )


ADDON_CHOICES = [
    "towel",
    "lock",
    "coffee",
    "breakfast",
    "parking",
    "cleaning",
    "taxi",
    "tour",
]


class AddonFactory(factory.django.DjangoModelFactory):
    """
    Creates an Addon for a property which we can easily use in tests or to attach to
    bookings.
    """

    class Meta:
        model = Addon
        django_get_or_create = ("name", "property")

    name = fuzzy.FuzzyChoice(ADDON_CHOICES)
    price = factory.Faker("random_int", min=1, max=20)
    property = factory.SubFactory(PropertyFactory)
    active = factory.Faker("boolean")
