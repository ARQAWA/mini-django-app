# Generated by Django 5.0.6 on 2024-06-27 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Миграция для изменения модели Play."""

    dependencies = [
        ("games", "0003_alter_account_info_alter_slot_account_and_more"),
        ("stats", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="play",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="play",
            name="balance",
            field=models.DecimalField(decimal_places=6, default=0, help_text="Stat Balance", max_digits=16),
        ),
        migrations.AddField(
            model_name="play",
            name="cards",
            field=models.BigIntegerField(default=0, help_text="Stat Bought Cards"),
        ),
        migrations.AddField(
            model_name="play",
            name="ciphers",
            field=models.BigIntegerField(default=0, help_text="Stat Ciphers"),
        ),
        migrations.AddField(
            model_name="play",
            name="combos",
            field=models.BigIntegerField(default=0, help_text="Stat Combos"),
        ),
        migrations.AddField(
            model_name="play",
            name="pph",
            field=models.DecimalField(decimal_places=6, default=0, help_text="Stat PPH", max_digits=16),
        ),
        migrations.AddField(
            model_name="play",
            name="taps",
            field=models.BigIntegerField(default=0, help_text="Stat Taps"),
        ),
        migrations.AddField(
            model_name="play",
            name="tasks",
            field=models.BigIntegerField(default=0, help_text="Stat Tasks"),
        ),
        migrations.AlterField(
            model_name="play",
            name="account",
            field=models.OneToOneField(
                help_text="Account", on_delete=django.db.models.deletion.RESTRICT, to="games.account"
            ),
        ),
        migrations.RemoveField(
            model_name="play",
            name="type",
        ),
    ]
