# Generated by Django 4.2 on 2024-12-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chain", "0007_alter_product_network_link"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="network_link",
        ),
        migrations.AddField(
            model_name="product",
            name="network_links",
            field=models.ManyToManyField(
                related_name="products",
                to="chain.networklink",
                verbose_name="Звенья сети",
            ),
        ),
    ]