# Generated by Django 4.2 on 2024-12-26 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chain", "0003_alter_networklink_options_alter_product_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="networklink",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="clients",
                to="chain.networklink",
                verbose_name="Поставщик",
            ),
        ),
    ]
