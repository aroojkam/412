# Generated by Django 5.1.6 on 2025-03-28 23:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
