import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from bookings.factories import (
    BookingConfirmedFactory,
    BookingFactory,
    BookingItemFactory,
)
from bookings.models import Booking, BookingItem


class BookingModelTests(TestCase):
    """
    Test suite for the Booking Model.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.booking = BookingFactory()
        cls.booking_items = BookingItemFactory.create_batch(size=2, booking=cls.booking)

    def test_setup_data_creation(self):
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(BookingItem.objects.count(), 2)
        self.assertEqual(self.booking.items.count(), 2)

    def test_str_representation(self):
        self.assertEqual(str(self.booking), f"Booking {self.booking.id}")

    def test_verbose_names(self):
        self.assertEqual(str(self.booking._meta.verbose_name), "Booking")
        self.assertEqual(str(self.booking._meta.verbose_name_plural), "Bookings")

    def test_booking_model_creation_is_accurate(self):
        booking_from_db = Booking.objects.first()

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking_from_db.first_name, self.booking.first_name)
        self.assertEqual(booking_from_db.last_name, self.booking.last_name)
        self.assertEqual(booking_from_db.email, self.booking.email)
        self.assertEqual(booking_from_db.whatsapp, self.booking.whatsapp)
        self.assertEqual(booking_from_db.residence, self.booking.residence)
        self.assertEqual(booking_from_db.paid, self.booking.paid)
        self.assertEqual(booking_from_db.payment_id, self.booking.payment_id)
        self.assertEqual(booking_from_db.discount, self.booking.discount)

    def test_max_length_of_all_fields(self):
        booking = Booking.objects.first()
        self.assertEqual(booking._meta.get_field("first_name").max_length, 50)
        self.assertEqual(booking._meta.get_field("last_name").max_length, 50)
        self.assertEqual(booking._meta.get_field("whatsapp").max_length, 17)
        self.assertEqual(booking._meta.get_field("payment_id").max_length, 250)

    def test_booking_objects_are_ordered_by_created_time(self):
        b_1 = Booking.objects.first()

        b_2 = BookingFactory()
        b_3 = BookingFactory()

        bookings = Booking.objects.all()

        self.assertEqual(bookings[0], b_3)
        self.assertEqual(bookings[1], b_2)
        self.assertEqual(bookings[2], b_1)
        self.assertEqual(b_1._meta.ordering, ("-created",))

    def test_confirmed_booking_factory_creation(self):
        booking = BookingConfirmedFactory()

        self.assertTrue(booking.paid)
        self.assertIsNotNone(booking.payment_id)

    def test_get_total_cost_calculation_is_accurate(self):
        expected = sum(item.get_cost() for item in self.booking_items)
        actual = self.booking.get_total_cost()

        self.assertEqual(expected, actual)

    def test_a_new_booking_has_zero_discount(self):
        self.assertEqual(self.booking.discount, Decimal(0))

    def test_a_new_booking_is_unpaid(self):
        self.assertFalse(self.booking.paid)

    def test_confirm_booking_works_correctly(self):
        """
        Main method where we try to confirm a booking when we get confirmation of
        payment from the webhook.

        It should mark the order as paid
        It should add the transaction id field
        """

        booking = BookingFactory()
        self.assertFalse(booking.paid)
        self.assertEqual(booking.payment_id, "")

        payment_id = uuid.uuid4()
        booking.confirm(payment_id=payment_id)

        self.assertTrue(booking.paid)
        self.assertIsNotNone(booking.payment_id)
        self.assertEqual(booking.payment_id, payment_id)


class BookingItemModelTests(TestCase):
    """Test suite for booking item model"""

    @classmethod
    def setUpTestData(cls):
        cls.booking = BookingFactory()
        cls.booking_items = BookingItemFactory.create_batch(size=2, booking=cls.booking)

    def test_setup_data_creation(self):
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(BookingItem.objects.count(), 2)
        self.assertEqual(self.booking.items.count(), 2)

    def test_str_representation(self):
        booking_item = self.booking_items[0]

        self.assertEqual(str(booking_item), f"Booking Item {booking_item.id}")

    def test_verbose_names(self):
        item = self.booking_items[0]

        self.assertEqual(str(item._meta.verbose_name), "Booking Item")
        self.assertEqual(str(item._meta.verbose_name_plural), "Booking Items")

    def test_booking_item_model_creation_is_correct(self):
        item_from_db = BookingItem.objects.first()
        item = self.booking_items[0]

        self.assertEqual(item_from_db.booking, item.booking)
        self.assertEqual(item_from_db.product, item.product)
        self.assertEqual(item_from_db.price, item.price)
        self.assertEqual(item_from_db.quantity, item.quantity)

    def test_booking_item_cost_is_correctly_calculated(self):
        item = self.booking_items[0]
        actual = item.get_cost()
        expected = item.price * item.quantity

        self.assertEqual(actual, expected)

    def test_order_item_min_max_quantity(self):
        # make quantity = 0
        booking_item = BookingItemFactory(booking=self.booking, quantity=0)

        with self.assertRaises(ValidationError):
            booking_item.full_clean()

        # make quantity = 20
        booking_item = BookingItemFactory(booking=self.booking, quantity=20)

        with self.assertRaises(ValidationError):
            booking_item.full_clean()
