# Generated by Django 4.2.8 on 2024-02-18 16:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stamp_fields", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fieldstypes",
            options={
                "ordering": ("-updated",),
                "verbose_name": "Поля печати",
                "verbose_name_plural": "Поля печати",
            },
        ),
        migrations.AlterModelOptions(
            name="groupoffieldstypes",
            options={
                "ordering": ("-updated",),
                "verbose_name": "Группа полей печати",
                "verbose_name_plural": "Группы полей печати",
            },
        ),
    ]