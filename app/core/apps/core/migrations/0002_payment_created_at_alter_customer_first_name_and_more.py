# Generated by Django 5.0.6 on 2024-06-28 17:09

from django.db import migrations, models


class Migration(migrations.Migration):
    """Миграция для добавления поля created_at в модель Payment и изменения полей модели Customer и Game."""

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text="Payment created at"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customer",
            name="first_name",
            field=models.CharField(help_text="First name"),
        ),
        migrations.AlterField(
            model_name="customer",
            name="last_name",
            field=models.CharField(help_text="Last name", null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="refresh_token",
            field=models.CharField(db_index=True, help_text="Refresh token"),
        ),
        migrations.AlterField(
            model_name="customer",
            name="username",
            field=models.CharField(help_text="Username", null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="id",
            field=models.CharField(help_text="Game ID", primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="game",
            name="name",
            field=models.CharField(help_text="Game name"),
        ),
        migrations.AlterField(
            model_name="payment",
            name="id",
            field=models.TextField(help_text="Payment ID", primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="payment",
            name="is_payed",
            field=models.BooleanField(db_index=True, help_text="Is payment payed"),
        ),
        migrations.AlterField(
            model_name="payment",
            name="type",
            field=models.CharField(choices=[("TON", "TON"), ("DEMO", "DEMO")], help_text="Payment type"),
        ),
    ]
