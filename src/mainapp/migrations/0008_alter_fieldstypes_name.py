# Generated by Django 4.2.8 on 2024-02-10 20:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0007_alter_fieldstypes_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fieldstypes",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Поле"),
        ),
    ]
