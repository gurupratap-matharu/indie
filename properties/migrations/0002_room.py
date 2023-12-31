# Generated by Django 4.2.6 on 2023-10-17 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=64, verbose_name="Name"),
                ),
                (
                    "grade",
                    models.CharField(
                        choices=[
                            ("BA", "Basic"),
                            ("ST", "Standard"),
                            ("DL", "Deluxe"),
                            ("SP", "Superior"),
                        ],
                        default="ST",
                        max_length=3,
                        verbose_name="Grade",
                    ),
                ),
                (
                    "num_of_guests",
                    models.PositiveSmallIntegerField(verbose_name="Number of Guests"),
                ),
                (
                    "room_type",
                    models.CharField(
                        choices=[
                            ("XD", "Mixed Dorm"),
                            ("MD", "Male Dorm"),
                            ("FD", "Female Dorm"),
                            ("PR", "Private Room"),
                            ("DB", "Double Bed"),
                            ("AP", "Apartment"),
                            ("FR", "Family Room"),
                            ("PT", "Private Tent"),
                            ("ST", "Shared Tent"),
                        ],
                        default="PR",
                        max_length=3,
                        verbose_name="Room Type",
                    ),
                ),
                (
                    "ensuite",
                    models.BooleanField(
                        default=True,
                        help_text="Does it have attached bathroom?",
                        verbose_name="Ensuite",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                (
                    "weekday_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="Weekday Price"
                    ),
                ),
                (
                    "weekend_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="Weekend Price"
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "room",
                "verbose_name_plural": "rooms",
            },
        ),
    ]
