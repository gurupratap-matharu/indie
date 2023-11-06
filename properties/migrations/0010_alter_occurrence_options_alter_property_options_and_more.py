# Generated by Django 4.2.6 on 2023-11-05 22:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0009_occurrence_unique_occurrence"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="occurrence",
            options={
                "ordering": ("for_date",),
                "verbose_name": "Occurrence",
                "verbose_name_plural": "Occurrences",
            },
        ),
        migrations.AlterModelOptions(
            name="property",
            options={
                "ordering": ["-created"],
                "verbose_name": "Property",
                "verbose_name_plural": "Properties",
            },
        ),
        migrations.AlterModelOptions(
            name="room",
            options={"verbose_name": "Room", "verbose_name_plural": "Rooms"},
        ),
        migrations.AddField(
            model_name="room",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="room",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="occurrence",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="occurrences",
                to="properties.room",
                verbose_name="Room",
            ),
        ),
    ]