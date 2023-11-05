from django.db import IntegrityError
from django.test import TestCase

from faker import Faker

from properties.factories import PropertyFactory
from properties.models import Property

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
        latitude, longitude = fake.latitude(), fake.longitude()
        _ = Property.objects.create(
            name="Mendoza hostel",
            slug="mendoza-hostel",
            latitude=latitude,
            longitude=longitude,
        )

        with self.assertRaises(IntegrityError):
            # repeat the same slug on purpose
            Property.objects.create(
                name="Hostel Mendoza",
                slug="mendoza-hostel",
                latitude=latitude,
                longitude=longitude,
            )


class RoomModelTests(TestCase):
    pass


class OccurrenceModelTests(TestCase):
    pass


class AddonModelTests(TestCase):
    pass
