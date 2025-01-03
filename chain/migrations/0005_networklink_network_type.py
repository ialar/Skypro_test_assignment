# Generated by Django 4.2 on 2024-12-27 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chain", "0004_alter_networklink_supplier"),
    ]

    operations = [
        migrations.AddField(
            model_name="networklink",
            name="network_type",
            field=models.CharField(
                choices=[
                    ("factory", "Завод"),
                    ("retail", "Розничная сеть"),
                    ("individual", "Индивидуальный предприниматель"),
                ],
                default="retail",
                max_length=10,
                verbose_name="Тип звена сети",
            ),
        ),
    ]
