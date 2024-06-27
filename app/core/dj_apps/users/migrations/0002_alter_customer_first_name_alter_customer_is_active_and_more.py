# Generated by Django 5.0.6 on 2024-06-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    """Миграция для изменения полей модели Customer."""

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="first_name",
            field=models.CharField(help_text="First name", max_length=150),
        ),
        migrations.AlterField(
            model_name="customer",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True, help_text="Is user active"),
        ),
        migrations.AlterField(
            model_name="customer",
            name="last_name",
            field=models.CharField(blank=True, help_text="Last name", max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="refresh_token",
            field=models.CharField(db_index=True, help_text="Refresh token", max_length=256),
        ),
        migrations.AlterField(
            model_name="customer",
            name="username",
            field=models.CharField(db_index=True, help_text="Username", max_length=150, unique=True),
        ),
    ]
