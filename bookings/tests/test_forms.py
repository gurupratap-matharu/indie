from django.test import SimpleTestCase

from bookings.forms import BookingForm


class BookingFormTests(SimpleTestCase):
    """
    Test suite for the booking model form.
    """

    def setUp(self):
        self.field_required_msg = "This field is required."
        self.form_data = {
            "first_name": "Isadora",
            "last_name": "Sobredo",
            "email": "isadorasobredo@gmail.com",
            "whatsapp": "+5491150223321",
            "residence": "AR",
        }

    def test_booking_form_is_valid_for_valid_data(self):
        form = BookingForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_empty_booking_form_raises_valid_error(self):
        form = BookingForm(data={})

        self.assertEqual(form.errors["first_name"][0], self.field_required_msg)
        self.assertEqual(form.errors["last_name"][0], self.field_required_msg)
        self.assertEqual(form.errors["email"][0], self.field_required_msg)
        self.assertEqual(form.errors["residence"][0], self.field_required_msg)
        self.assertEqual(form.errors["whatsapp"][0], self.field_required_msg)

    def test_booking_form_is_invalid_for_missing_first_name_field(self):
        self.form_data.pop("first_name")
        form = BookingForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_is_invalid_for_missing_last_name_field(self):
        self.form_data.pop("last_name")
        form = BookingForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_is_invalid_for_missing_email_field(self):
        self.form_data.pop("email")
        form = BookingForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_is_invalid_for_missing_residence_field(self):
        self.form_data.pop("residence")
        form = BookingForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_is_invalid_for_missing_whatsapp_field(self):
        self.form_data.pop("whatsapp")
        form = BookingForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_fields_are_cleaned_correctly(self):
        form = BookingForm(
            data={
                "first_name": "     RoMiNa ",
                "last_name": "   Pistolesi",
                "email": "         ROMI@email.com               ",
                "residence": "AR",
                "whatsapp": "+549112321232",
            }
        )

        self.assertTrue(form.is_valid())  # trigger the clean
        
        self.assertEqual(form.cleaned_data["first_name"], "Romina")
        self.assertEqual(form.cleaned_data["last_name"], "Pistolesi")
        self.assertEqual(form.cleaned_data["email"], "romi@email.com")
