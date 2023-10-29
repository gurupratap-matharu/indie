import factory
from faker import Faker

from .models import Booking, BookingItem

fake = Faker()


class BookingFactory(factory.django.DjangoModelFactory):
    """
    Factory to create fake bookings in the platform.
    """

    class Meta:
        model = Booking

    first_name = factory.Faker("first_name_nonbinary")
    last_name = factory.Faker("last_name_nonbinary")
    email = factory.LazyAttribute(
        lambda o: "%s-%s@email.com" % (o.first_name.lower(), o.last_name.lower())
    )
    residence = factory.Faker("country_code")
    whatsapp = factory.LazyAttribute(
        lambda _: (fake.country_calling_code() + fake.phone_number())[:14]
    )


class BookingConfirmedFactory(BookingFactory):
    """Create a confirmed booking with a dummy payment id"""

    paid = True
    payment_id = factory.Faker("bban")


class BookingItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create individual booking items.
    """

    class Meta:
        model = BookingItem

    booking = factory.SubFactory(BookingFactory)
    product = factory.SubFactory("properties.factories.RoomFactory")
    price = factory.LazyAttribute(lambda o: o.product.weekday_price)
    quantity = factory.Faker("random_int", min=1, max=8)


def booking_dict():
    """Handy method to return a dummy booking as a dict"""

    return factory.build(dict, FACTORY_CLASS=BookingFactory)


def booking_confirmed_dict():
    return factory.build(dict, FACTORY_CLASS=BookingConfirmedFactory)


def booking_item_dict():
    """Handy method to return a dummy booking item as a dict"""

    return factory.build(dict, FACTORY_CLASS=BookingItemFactory)
