from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from faker import Faker

from properties.factories import (
    AddonFactory,
    OccurrenceFactory,
    PropertyFactory,
    RoomFactory,
)
from properties.models import Addon, Occurrence, Property, Room

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
        cls.today = timezone.localdate()
        cls.tomorrow = cls.today + timedelta(days=1)
        cls.day_after = cls.today + timedelta(days=2)

        cls.property = PropertyFactory()
        cls.rooms = RoomFactory.create_batch(size=2, property=cls.property)

        # Create different rates for all occurrences for one room
        cls.room = cls.rooms[0]
        cls.rate_today, cls.rate_tmrw, cls.rate_day_after = 10, 15, 20
        cls.av_today, cls.av_tmrw, cls.av_day_after = 4, 3, 2

        cls.occurrences = [
            # Today
            OccurrenceFactory(
                room=cls.room,
                for_date=cls.today,
                rate=cls.rate_today,
                availability=cls.av_today,
            ),
            # Tomorrow
            OccurrenceFactory(
                room=cls.room,
                for_date=cls.tomorrow,
                rate=cls.rate_tmrw,
                availability=cls.av_tmrw,
            ),
            # Day after
            OccurrenceFactory(
                room=cls.room,
                for_date=cls.day_after,
                rate=cls.rate_day_after,
                availability=cls.av_day_after,
            ),
        ]

    def test_setup_data_creation(self):
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Room.objects.count(), 2)
        self.assertEqual(self.property.rooms.count(), 2)

    def test_str_representation(self):
        room = self.rooms[0]
        self.assertEqual(str(room), f"{room.name}")

    def test_verbose_names(self):
        room = self.rooms[0]
        self.assertEqual(str(room._meta.verbose_name), "Room")
        self.assertEqual(str(room._meta.verbose_name_plural), "Rooms")

    def test_schedule_url(self):
        room = self.rooms[0]
        actual = room.get_schedule_url()
        expected = f"/portal/{self.property.slug}/schedule/rooms/{room.id}/"

        self.assertEqual(actual, expected)

    def test_add_to_cart_url(self):
        room = self.rooms[0]
        actual = room.get_add_to_cart_url()
        expected = f"/cart/add/{room.id}/"

        self.assertEqual(actual, expected)

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

    # get_cost()
    def test_room_get_cost_for_multiple_nights_works_correctly(self):
        """
        A room may have different pricing over weekends (fri, sat)

        When being booked for multiple nights say thu, fri, sat, sun this method
        should calculate cost of each night and sum it up correctly.
        """

        actual = self.room.get_cost(start=self.today, end=self.day_after)
        expected = self.rate_today + self.rate_tmrw + self.rate_day_after

        self.assertEqual(actual, expected)

    def test_room_get_cost_for_only_one_night_works_correctly(self):
        actual = self.room.get_cost(start=self.today, end=self.today)
        expected = self.rate_today

        self.assertEqual(actual, expected)

    def test_room_get_cost_for_two_nights_works_correctly(self):
        actual = self.room.get_cost(start=self.today, end=self.tomorrow)
        expected = self.rate_today + self.rate_tmrw

        self.assertEqual(actual, expected)

    def test_room_get_cost_raises_exception_for_invalid_input(self):
        with self.assertRaises(ValidationError):
            # end date < start date
            self.room.get_cost(start=self.tomorrow, end=self.today)

    # get_availability()
    def test_room_get_availability_for_multiple_nights_works_correctly(self):
        actual = self.room.get_availability(start=self.today, end=self.day_after)
        expected = min(self.av_today, self.av_tmrw, self.av_day_after)

        self.assertEqual(actual, expected)

    def test_room_get_availability_for_two_nights_works_correctly(self):
        actual = self.room.get_availability(start=self.today, end=self.tomorrow)
        expected = min(self.av_today, self.av_tmrw)

        self.assertEqual(actual, expected)

    def test_room_get_availability_for_one_night_works_correctly(self):
        actual = self.room.get_availability(start=self.today, end=self.today)
        expected = self.av_today

        self.assertEqual(actual, expected)

    def test_room_get_availability_raises_exception_for_invalid_input(self):
        with self.assertRaises(ValidationError):
            # end date < start date
            self.room.get_availability(start=self.tomorrow, end=self.today)

    def test_room_type_is_identified_correctly_for_shared_dorm_rooms(self):
        room_1 = RoomFactory(room_type=Room.MIXED_DORM)
        room_2 = RoomFactory(room_type=Room.FEMALE_DORM)
        room_3 = RoomFactory(room_type=Room.MALE_DORM)

        self.assertTrue(room_1.is_dorm())
        self.assertTrue(room_2.is_dorm())
        self.assertTrue(room_3.is_dorm())

        self.assertFalse(room_1.is_private())
        self.assertFalse(room_2.is_private())
        self.assertFalse(room_3.is_private())

    def test_room_type_is_identified_correctly_for_private_rooms(self):
        room_1 = RoomFactory(room_type=Room.PRIVATE_ROOM)
        room_2 = RoomFactory(room_type=Room.PRIVATE_TENT)
        room_3 = RoomFactory(room_type=Room.DOUBLE_BED)

        self.assertTrue(room_1.is_private())
        self.assertTrue(room_2.is_private())
        self.assertTrue(room_3.is_private())

        self.assertFalse(room_1.is_dorm())
        self.assertFalse(room_2.is_dorm())
        self.assertFalse(room_3.is_dorm())


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
        self.assertEqual(str(occ), f"Occ: {occ.for_date}")

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
            Occurrence.objects.create(room=self.room, for_date=self.today)

    def test_occurrence_rate_is_always_positive(self):
        # make rate = 0
        next_week = self.today + timedelta(days=7)
        occ = OccurrenceFactory(room=self.room, for_date=next_week, rate=0)

        with self.assertRaises(ValidationError) as cm:
            occ.full_clean()

        exc = cm.exception
        error_msg = exc.message_dict.get("rate")[0]
        self.assertEqual(error_msg, "Ensure this value is greater than or equal to 1.")

    def test_occurrence_availability_cannot_be_less_than_zero(self):
        next_month = self.today + timedelta(days=30)

        with self.assertRaises(IntegrityError):
            # set availability less than zero
            # note here we check for IntegrityError and not ValidationError
            OccurrenceFactory(room=self.room, for_date=next_month, availability=-1)

    def test_occurrence_availability_upper_limit(self):
        next_month = self.today + timedelta(days=30)

        with self.assertRaises(ValidationError):
            # Set availability > 20
            # Upper limit is checked in validators so we need to assert ValidationError
            # instead of IntegrityError.
            # Also full_clean() method needs to be called to run the validator
            occ = OccurrenceFactory(
                room=self.room, for_date=next_month, availability=21
            )
            occ.full_clean()


class AddonModelTests(TestCase):
    """
    Test suite for Addon model
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.property = PropertyFactory()
        cls.addon = AddonFactory(name="Breakfast", property=cls.property)

    def test_setup_data_creation(self):
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Addon.objects.count(), 1)

    def test_str_representation(self):
        self.assertEqual(str(self.addon), f"{self.addon.name}: {self.addon.price}")

    def test_verbose_names(self):
        self.assertEqual(str(self.addon._meta.verbose_name), "Addon")
        self.assertEqual(str(self.addon._meta.verbose_name_plural), "Addons")

    def test_addon_model_creation_is_accurate(self):
        addon = Addon.objects.first()

        self.assertEqual(addon.property, self.addon.property)
        self.assertEqual(addon.name, self.addon.name)
        self.assertEqual(addon.icon, self.addon.icon)
        self.assertEqual(addon.price, self.addon.price)
        self.assertEqual(addon.active, self.addon.active)

    def test_max_length_of_all_fields(self):
        obj = Addon.objects.first()
        self.assertEqual(obj._meta.get_field("name").max_length, 64)
        self.assertEqual(obj._meta.get_field("icon").max_length, 64)

        self.assertEqual(obj._meta.get_field("price").max_digits, 12)
        self.assertEqual(obj._meta.get_field("price").decimal_places, 2)

    def test_addon_price_cannot_be_zero_or_negative(self):
        with self.assertRaises(ValidationError):
            addon = AddonFactory(property=self.property, price=0)
            addon.full_clean()

        with self.assertRaises(ValidationError):
            addon = AddonFactory(property=self.property, price=-1)
            addon.full_clean()

    def test_addon_objects_are_ordered_by_name(self):
        a_1 = Addon.objects.first()

        a_2 = AddonFactory(name="Taxi", property=self.property)
        a_3 = AddonFactory(name="Coffee", property=self.property)

        objs = Addon.objects.all()

        self.assertEqual(objs[0], a_1)  # name = "Breakfast"
        self.assertEqual(objs[1], a_3)  # name = "Coffee"
        self.assertEqual(objs[2], a_2)  # name = "Taxi"

        self.assertEqual(a_1._meta.ordering, ("name",))

    def test_addon_is_unique_for_a_given_property(self):
        # We have an addon called `breakfast` for our property
        # Creating another one should violate the unique constraint

        with self.assertRaises(IntegrityError):
            # Veer here we don't use the factory since it uses django_get_or_create
            # So it won't try to create another addon for the same property
            Addon.objects.create(
                name="Breakfast", price=Decimal(1), property=self.property
            )
