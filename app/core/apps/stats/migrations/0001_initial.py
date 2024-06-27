# Generated by Django 5.0.6 on 2024-06-27 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Миграция для создания модели Play."""

    initial = True

    dependencies = [
        ("games", "0003_alter_account_info_alter_slot_account_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Play",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(
                        choices=[("LIFETIME", "Lifetime"), ("SESSION", "Session")],
                        help_text="Stats Type",
                        max_length=32,
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        help_text="Account", on_delete=django.db.models.deletion.RESTRICT, to="games.account"
                    ),
                ),
            ],
            options={
                "unique_together": {("account", "type")},
            },
        ),
    ]
