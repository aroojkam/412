# Generated by Django 5.1.6 on 2025-02-23 04:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="image",
        ),
        migrations.AddField(
            model_name="profile",
            name="image_url",
            field=models.URLField(default="https://via.placeholder.com/150"),
        ),
    ]
