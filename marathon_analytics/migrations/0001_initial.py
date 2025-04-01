# Generated by Django 5.1.6 on 2025-04-01 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Result",
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
                ("bib", models.IntegerField()),
                ("first_name", models.TextField()),
                ("last_name", models.TextField()),
                ("ctz", models.TextField()),
                ("city", models.TextField()),
                ("state", models.TextField()),
                ("gender", models.CharField(max_length=6)),
                ("division", models.CharField(max_length=6)),
                ("place_overall", models.IntegerField()),
                ("place_gender", models.IntegerField()),
                ("place_division", models.IntegerField()),
                ("start_time_of_day", models.TimeField()),
                ("finish_time_of_day", models.TimeField()),
                ("time_finish", models.TimeField()),
                ("time_half1", models.TimeField()),
                ("time_half2", models.TimeField()),
            ],
        ),
    ]
