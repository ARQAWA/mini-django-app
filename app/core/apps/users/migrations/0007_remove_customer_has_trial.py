# Generated by Django 5.0.6 on 2024-06-28 08:53

from django.db import migrations


class Migration(migrations.Migration):
    """Миграция для удаления поля has_trial из модели Customer."""

    dependencies = [
        ("users", "0006_remove_customer_has_banned"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="has_trial",
        ),
    ]
