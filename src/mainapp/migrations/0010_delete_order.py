# Generated by Django 4.2.8 on 2024-02-11 21:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0009_order"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Order",
        ),
    ]
