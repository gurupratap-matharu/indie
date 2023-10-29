from decimal import Decimal

from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy

from coupons.factories import CouponFactory
from trips.factories import TripFactory

from cart.cart import Cart, CartException


class SessionDict(dict):
    """Dummy session dict to be attached to request factory"""

    modified = False


class CartTests(TestCase):
    """
    Test Suite for the main cart class and all its methods.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse_lazy("cart:cart_detail"))

        # Session manually supplied for request generated by RequestFactory
        self.trips = {
            "616e207c-c4f2-4fec-9b66-8ed779914e08": {
                "quantity": 1,
                "price": "18357.82",
            },
            "bdae1946-2c22-4d7f-9b0e-ef8f4e9f65dc": {
                "quantity": 3,
                "price": "9851.53",
            },
        }
        self.coupon = CouponFactory()

        self.request.session = SessionDict()  # type:ignore
        self.request.session["cart"] = self.trips
        self.request.session["coupon_id"] = str(self.coupon.id)  # type:ignore

    def test_cart_is_initialized_correctly_for_empty_session(self):
        self.request.session.clear()
        cart = Cart(self.request)

        self.assertEqual(self.request.session["cart"], {})
        self.assertEqual(cart.cart, {})

    def test_existing_cart_in_session_is_correctly_parsed(self):
        # aliasing for simplicity
        request = self.request
        session = self.request.session

        # Act: instantiate the cart
        cart = Cart(request)

        # Assert: cart object has the session cart and coupon
        self.assertEqual(cart.cart, session["cart"])
        self.assertEqual(cart.coupon_id, session["coupon_id"])

    def test_cart_coupon_property(self):
        cart = Cart(self.request)

        self.assertEqual(cart.coupon, self.coupon)
        self.assertEqual(cart.coupon_id, str(self.coupon.id))

    def test_cart_discount_is_correctly_calculated_from_valid_coupon(self):
        cart = Cart(self.request)

        discount = self.coupon.discount
        actual = cart.get_discount()
        expected = (discount / Decimal(100)) * cart.get_total_price()  # type:ignore

        self.assertEqual(actual, expected)

    def test_cart_discount_is_zero_for_empty_coupon(self):
        """
        Remove the coupon_id from the session first and check the discount
        """
        del self.request.session["coupon_id"]

        cart = Cart(self.request)

        self.assertIsNone(cart.coupon_id)
        self.assertIsNone(cart.coupon)

        discount = cart.get_discount()
        self.assertEqual(Decimal(0), discount)

    def test_cart_discount_is_zero_for_invalid_coupon(self):
        self.request.session["coupon_id"] = "1234"  # invalid coupon id

        cart = Cart(self.request)

        self.assertIsNone(cart.coupon)

        discount = cart.get_discount()
        self.assertEqual(Decimal(0), discount)

    def test_adding_a_trip_to_cart_works(self):
        """
        We start with an empty session and add a trip later
        """
        self.request.session.clear()

        trip = TripFactory()
        trip_id = str(trip.id)

        cart = Cart(self.request)
        cart.add(trip=trip, quantity=2)

        self.assertEqual(cart.cart[trip_id], {"quantity": 2, "price": str(trip.price)})

    def test_adding_a_trip_to_cart_is_idempotent(self):
        self.request.session.clear()

        trip = TripFactory()
        trip_id = str(trip.id)
        cart = Cart(self.request)
        cart.add(trip=trip, quantity=2, override_quantity=True)

        # should only update quantity
        cart.add(trip=trip, quantity=5, override_quantity=True)

        # Assert: cart has only one trip
        # Assert: cart has 5 passengers
        # Assert: cart has only one trip
        self.assertEqual(cart.cart[trip_id], {"quantity": 5, "price": str(trip.price)})
        self.assertEqual(len(cart), 5)
        self.assertEqual(len(cart.cart), 1)

    def test_user_can_add_maximum_two_trips_to_cart(self):
        cart = Cart(self.request)
        # Cart already has two trips. Let's try adding another one
        trip = TripFactory()

        with self.assertRaises(CartException):
            cart.add(trip=trip, override_quantity=True)

    def test_removing_an_existing_trip_from_cart_works(self):
        """
        Clear the session and create a trip.
        Add it to cart and verify all ok
        Remove the trip from cart and make sure it works.
        """

        self.request.session.clear()

        trip = TripFactory()
        trip_id = str(trip.id)

        cart = Cart(self.request)
        cart.add(trip=trip, quantity=2, override_quantity=True)

        self.assertIn(trip_id, cart.cart)

        # now remove the trip and check its not in cart
        cart.remove(trip=trip)

        self.assertNotIn(trip, cart.cart)

    def test_removing_a_non_existing_trip_from_cart_has_no_effect(self):
        cart = Cart(self.request)
        trip = TripFactory()  # 👈 this trip is not added to cart

        self.assertEqual(len(cart), 4)  # num of passengers
        self.assertEqual(len(cart.cart), 2)  # num of trips

        cart.remove(trip=trip)
        # make sure removal has no effect
        self.assertEqual(len(cart), 4)  # num of passengers
        self.assertEqual(len(cart.cart), 2)  # num of trips

    def test_saving_a_cart_works(self):
        cart = Cart(self.request)
        self.assertFalse(cart.session.modified)

        cart.save()
        self.assertTrue(cart.session.modified)

    def test_clearing_a_cart_removes_all_trips_from_cart(self):
        cart = Cart(self.request)

        self.assertEqual(len(cart), 4)  # num of passengers
        self.assertEqual(len(cart.cart), 2)  # num of trips

        cart.clear()
        self.assertNotIn("cart", cart.session)

        # We need to instantiate the cart again as the session itself was cleared
        cart = Cart(self.request)

        self.assertEqual(len(cart), 0)
        self.assertEqual(len(cart.cart), 0)

    def test_get_total_price_works_correctly(self):
        cart = Cart(self.request)

        expected = sum(
            Decimal(item["price"]) * item["quantity"] for item in cart.cart.values()
        )
        actual = cart.get_total_price()

        self.assertEqual(actual, expected)

    def test_get_total_price_after_discount_works_correctly(self):
        cart = Cart(self.request)

        actual = cart.get_total_price_after_discount()
        expected = cart.get_total_price() - cart.get_discount()

        self.assertEqual(actual, expected)

    def test_len_of_cart_is_correctly_calculated(self):
        cart = Cart(self.request)

        self.assertEqual(len(cart), 4)  # num of passengers
        self.assertEqual(len(cart.cart), 2)  # num of trips

    def test_cart_can_be_iterated_correctly(self):
        cart = Cart(self.request)
        expected = [v for k, v in self.trips.items()]

        self.assertEqual(list(cart), expected)
