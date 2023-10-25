from django.template.defaultfilters import slugify

import factory
from django_countries import countries
from factory import fuzzy

from users.factories import PropertyOwnerFactory

from .models import Property


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
