# Generated by Django 4.2.6 on 2023-11-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0008_alter_occurrence_availability_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="occurrence",
            constraint=models.UniqueConstraint(
                fields=("room", "for_date"), name="unique_occurrence"
            ),
        ),
    ]
