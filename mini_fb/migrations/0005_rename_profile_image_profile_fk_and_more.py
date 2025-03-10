# Generated by Django 5.1.6 on 2025-03-06 00:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mini_fb", "0004_image_statusimage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image",
            old_name="profile",
            new_name="profile_fk",
        ),
        migrations.RenameField(
            model_name="image",
            old_name="timestamp",
            new_name="time_stamp",
        ),
        migrations.RenameField(
            model_name="statusimage",
            old_name="StatusMessage",
            new_name="StatusMessage_fk",
        ),
        migrations.RenameField(
            model_name="statusimage",
            old_name="image",
            new_name="image_fk",
        ),
        migrations.AlterField(
            model_name="image",
            name="caption",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="image",
            name="image_file",
            field=models.ImageField(blank=True, upload_to="images/"),
        ),
    ]
