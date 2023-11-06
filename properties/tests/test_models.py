import pdb
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from faker import Faker

from properties.factories import OccurrenceFactory, PropertyFactory, RoomFactory
from properties.models import Occurrence, Property, Room

fake = Faker()


class PropertyModelTests(TestCase):
    """
    Test suite for the property model.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.property = PropertyFactory()

    def test_setup_data_creation(self):
        self.assertEqual(Property.objects.count(), 1)

    def test_str_representation(self):
        self.assertEqual(str(self.property), f"{self.property.name}")

    def test_verbose_names(self):
        self.assertEqual(str(self.property._meta.verbose_name), "Property")
        self.assertEqual(str(self.property._meta.verbose_name_plural), "Properties")

    def test_absolute_url(self):
        actual = self.property.get_absolute_url()
        expected = f"/properties/{self.property.slug}/"
        self.assertEqual(actual, expected)

    def test_portal_url(self):
        actual = self.property.get_portal_url()
        expected = f"/portal/{self.property.slug}/"

        self.assertEqual(actual, expected)

    def test_property_model_creation_is_accurate(self):
        property_from_db = Property.objects.first()

        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(property_from_db.name, self.property.name)
        self.assertEqual(property_from_db.owner, self.property.owner)
        self.assertEqual(property_from_db.slug, self.property.slug)
        self.assertEqual(property_from_db.description, self.property.description)
        self.assertEqual(property_from_db.property_type, self.property.property_type)
        self.assertEqual(property_from_db.website, self.property.website)
        self.assertEqual(property_from_db.address_line1, self.property.address_line1)
        self.assertEqual(property_from_db.address_line2, self.property.address_line2)
        self.assertEqual(property_from_db.city, self.property.city)
        self.assertEqual(property_from_db.state, self.property.state)
        self.assertEqual(property_from_db.postal_code, self.property.postal_code)
        self.assertEqual(property_from_db.country, self.property.country)
        self.assertEqual(property_from_db.phone, self.property.phone)
        self.assertEqual(property_from_db.email, self.property.email)
        self.assertEqual(
            round(property_from_db.latitude, 5), round(self.property.latitude, 5)
        )
        self.assertEqual(
            round(property_from_db.longitude, 5), round(self.property.longitude, 5)
        )
        self.assertEqual(property_from_db.legal_entity, self.property.legal_entity)
        self.assertEqual(property_from_db.tax_id, self.property.tax_id)
        self.assertEqual(property_from_db.active, self.property.active)

    def test_max_length_of_all_fields(self):
        obj = Property.objects.first()
        self.assertEqual(obj._meta.get_field("name").max_length, 200)
        self.assertEqual(obj._meta.get_field("slug").max_length, 200)
        self.assertEqual(obj._meta.get_field("property_type").max_length, 10)
        self.assertEqual(obj._meta.get_field("address_line1").max_length, 128)
        self.assertEqual(obj._meta.get_field("address_line2").max_length, 128)
        self.assertEqual(obj._meta.get_field("city").max_length, 64)
        self.assertEqual(obj._meta.get_field("state").max_length, 40)
        self.assertEqual(obj._meta.get_field("postal_code").max_length, 10)
        self.assertEqual(obj._meta.get_field("phone").max_length, 17)

        self.assertEqual(obj._meta.get_field("latitude").max_digits, 9)
        self.assertEqual(obj._meta.get_field("longitude").max_digits, 9)

        self.assertEqual(obj._meta.get_field("latitude").decimal_places, 6)
        self.assertEqual(obj._meta.get_field("longitude").decimal_places, 6)

    def test_property_objects_are_ordered_by_created_time(self):
        p_1 = Property.objects.first()
        p_2, p_3 = PropertyFactory.create_batch(size=2)

        objs = Property.objects.all()

        self.assertEqual(objs[0], p_3)
        self.assertEqual(objs[1], p_2)
        self.assertEqual(objs[2], p_1)

        self.assertEqual(p_1._meta.ordering, ["-created"])

    def test_property_slug_is_auto_generated_even_if_not_supplied(self):
        latitude, longitude = fake.latitude(), fake.longitude()
        obj = Property.objects.create(
            name="sabatico hostel buenos aires", latitude=latitude, longitude=longitude
        )

        self.assertEqual(obj.slug, "sabatico-hostel-buenos-aires")

    def test_existing_slug_is_not_overwritten_when_updating_property(self):
        latitude, longitude = fake.latitude(), fake.longitude()
        obj = Property.objects.create(
            name="sabatico hostel buenos aires", latitude=latitude, longitude=longitude
        )
        self.assertEqual(obj.slug, "sabatico-hostel-buenos-aires")

        # update the name
        obj, created = Property.objects.update_or_create(
            name="sabatico hostel buenos aires",
            defaults={"name": "The new SABATICO"},
        )
        # make sure slug remains the same
        self.assertEqual(obj.slug, "sabatico-hostel-buenos-aires")

    def test_all_properties_have_unique_slugs(self):
        obj = Property.objects.first()
        # Check unique is defined on slug field
        self.assertTrue(obj._meta.get_field("slug").unique)

        latitude, longitude = fake.latitude(), fake.longitude()
        _ = Property.objects.create(
            name="Mendoza hostel",
            slug="mendoza-hostel",
            latitude=latitude,
            longitude=longitude,
        )

        # repeating the same slug should raise Integrity Error
        with self.assertRaises(IntegrityError):
            Property.objects.create(
                name="Hostel Mendoza",
                slug="mendoza-hostel",
                latitude=latitude,
                longitude=longitude,
            )


class RoomModelTests(TestCase):
    """
    Test suite for the Room Model
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.property = PropertyFactory()
        cls.rooms = RoomFactory.create_batch(size=2, property=cls.property)

    def test_setup_data_creation(self):
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Room.objects.count(), 2)
        self.assertEqual(self.property.rooms.count(), 2)

    def test_str_representation(self):
        room = self.rooms[0]
        self.assertEqual(str(room), f"{self.property} | {room.name}")

    def test_verbose_names(self):
        room = self.rooms[0]
        self.assertEqual(str(room._meta.verbose_name), "Room")
        self.assertEqual(str(room._meta.verbose_name_plural), "Rooms")

    def test_room_model_creation_is_correct(self):
        room = self.rooms[0]
        room_from_db = Room.objects.get(id=room.id)

        self.assertEqual(room_from_db.name, room.name)
        self.assertEqual(room_from_db.grade, room.grade)
        self.assertEqual(room_from_db.num_of_guests, room.num_of_guests)
        self.assertEqual(room_from_db.room_type, room.room_type)
        self.assertEqual(room_from_db.ensuite, room.ensuite)
        self.assertEqual(room_from_db.description, room.description)
        self.assertEqual(room_from_db.weekday_price, room.weekday_price)
        self.assertEqual(room_from_db.weekend_price, room.weekend_price)
        self.assertEqual(room_from_db.active, room.active)

    def test_max_length_of_all_fields(self):
        obj = Room.objects.first()

        self.assertEqual(obj._meta.get_field("name").max_length, 64)
        self.assertEqual(obj._meta.get_field("grade").max_length, 3)
        self.assertEqual(obj._meta.get_field("room_type").max_length, 3)

        self.assertEqual(obj._meta.get_field("weekday_price").max_digits, 12)
        self.assertEqual(obj._meta.get_field("weekend_price").max_digits, 12)

        self.assertEqual(obj._meta.get_field("weekday_price").decimal_places, 2)
        self.assertEqual(obj._meta.get_field("weekend_price").decimal_places, 2)

    def test_room_objects_are_ordered_by_property_and_room_type(self):
        room = Room.objects.first()

        self.assertEqual(room._meta.ordering, ("property", "room_type"))

    def test_room_price_is_greater_than_zero(self):
        # make price = 0
        room = RoomFactory(property=self.property, weekday_price=0)

        with self.assertRaises(ValidationError) as cm:
            room.full_clean()

        exc = cm.exception
        error_msg = exc.message_dict.get("weekday_price")[0]
        self.assertEqual(error_msg, "Ensure this value is greater than or equal to 1.")


class OccurrenceModelTests(TestCase):
    """
    Test suite for the occurrence model.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.today = timezone.localdate()
        cls.tomorrow = cls.today + timedelta(days=1)
        cls.day_after = cls.today + timedelta(days=2)

        cls.property = PropertyFactory()
        cls.room = RoomFactory(property=cls.property)
        cls.occurrences = [
            OccurrenceFactory(room=cls.room, for_date=cls.today),
            OccurrenceFactory(room=cls.room, for_date=cls.tomorrow),
            OccurrenceFactory(room=cls.room, for_date=cls.day_after),
        ]

    def test_setup_data_creation(self):
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Occurrence.objects.count(), 3)

        self.assertEqual(self.room.occurrences.count(), 3)

    def test_str_representation(self):
        occ = self.occurrences[0]
        self.assertEqual(str(occ), f"{self.room} | {occ.for_date}")

    def test_verbose_names(self):
        occ = self.occurrences[0]
        self.assertEqual(str(occ._meta.verbose_name), "Occurrence")
        self.assertEqual(str(occ._meta.verbose_name_plural), "Occurrences")

    def test_occurrence_objects_are_compared_via_date(self):
        occ_today, occ_tomorrow, occ_day_after = self.occurrences

        self.assertTrue(occ_today < occ_tomorrow)
        self.assertTrue(occ_tomorrow < occ_day_after)
        self.assertFalse(occ_day_after < occ_today)

    def test_occurrence_model_creation_is_correct(self):
        occ = self.occurrences[0]
        occ_from_db = Occurrence.objects.get(id=occ.id)

        self.assertEqual(occ_from_db.rate, occ.rate)
        self.assertEqual(occ_from_db.availability, occ.availability)
        self.assertEqual(occ_from_db.room, occ.room)
        self.assertEqual(occ_from_db.for_date, occ.for_date)

    def test_max_length_of_all_fields(self):
        obj = Occurrence.objects.first()

        self.assertEqual(obj._meta.get_field("rate").max_digits, 12)
        self.assertEqual(obj._meta.get_field("rate").decimal_places, 2)

    def test_occurrence_objects_are_ordered_by_date(self):
        o_1, o_2, o_3 = self.occurrences

        objs = Occurrence.objects.all()

        self.assertEqual(objs[0], o_1)
        self.assertEqual(objs[1], o_2)
        self.assertEqual(objs[2], o_3)

        occ = Occurrence.objects.first()
        self.assertEqual(occ._meta.ordering, ("for_date",))

    def test_occurrence_is_unique_for_a_given_room_and_date(self):
        # We already have an occurrence for our room for today created in setup
        # Creating another one should violate the unique constraint

        with self.assertRaises(IntegrityError):
            OccurrenceFactory(room=self.room, for_date=self.today)

    def test_occurrence_rate_is_always_positive(self):
        # make rate = 0
        next_week = self.today + timedelta(days=7)
        occ = OccurrenceFactory(room=self.room, for_date=next_week, rate=0)

        with self.assertRaises(ValidationError) as cm:
            occ.full_clean()

        exc = cm.exception
        error_msg = exc.message_dict.get("rate")[0]
        self.assertEqual(error_msg, "Ensure this value is greater than or equal to 1.")

    def test_occurrence_availability_min_max_values(self):
        next_month = self.today + timedelta(days=30)

        # set availability less than zero
        occ = OccurrenceFactory(room=self.room, for_date=next_month, availability=-1)

        with self.assertRaises(IntegrityError) as cm:
            occ.full_clean()

        exc = cm.exception
        error_msg = exc.message_dict.get("availability")[0]
        self.assertEqual(error_msg, "Ensure this value is greater than or equal to 1.")


class AddonModelTests(TestCase):
    pass
