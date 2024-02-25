# Generated by Django 5.0.2 on 2024-02-25 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0011_rename_person_image_peoplegetallresult_box_result_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LicensePlateResult",
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
                ("image", models.CharField(max_length=500)),
                ("license_plate", models.CharField(max_length=64)),
            ],
        ),
    ]