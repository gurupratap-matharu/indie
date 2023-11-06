# Generated by Django 4.2.6 on 2023-11-04 20:14

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0007_occurrence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="occurrence",
            name="availability",
            field=models.PositiveIntegerField(
                default=1,
                validators=[django.core.validators.MaxValueValidator(20)],
                verbose_name="Availability",
            ),
        ),
        migrations.AlterField(
            model_name="occurrence",
            name="for_date",
            field=models.DateField(
                help_text="The date for the night the guest will stay at the property",
                validators=[
                    django.core.validators.MinValueValidator(
                        limit_value=django.utils.timezone.localdate
                    )
                ],
                verbose_name="For Date",
            ),
        ),
        migrations.AlterField(
            model_name="occurrence",
            name="rate",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Rate",
            ),
        ),
    ]
