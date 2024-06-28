# Generated by Django 5.0.6 on 2024-06-28 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Миграция для добавления поля PPHD в модель Play."""

    dependencies = [
        ("games", "0004_alter_account_customer_alter_account_game"),
        ("stats", "0002_alter_network_account_alter_play_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="play",
            name="pphd",
            field=models.BigIntegerField(default=0, help_text="Stat PPHD"),
        ),
        migrations.AlterField(
            model_name="network",
            name="account",
            field=models.OneToOneField(
                help_text="Account",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="network",
                to="games.account",
            ),
        ),
        migrations.AlterField(
            model_name="play",
            name="account",
            field=models.OneToOneField(
                help_text="Account",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="play",
                to="games.account",
            ),
        ),
        migrations.AlterField(
            model_name="play",
            name="balance",
            field=models.BigIntegerField(default=0, help_text="Balance"),
        ),
        migrations.AlterField(
            model_name="play",
            name="pph",
            field=models.BigIntegerField(default=0, help_text="PPH"),
        ),
    ]
