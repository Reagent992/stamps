# Generated by Django 4.2.14 on 2024-07-21 13:15

import core.abstract_models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("printy", "0002_alter_printy_group_alter_printy_published_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="printy",
            name="image",
            field=models.ImageField(
                upload_to=core.abstract_models.get_renamed_image_path,
                verbose_name="Картинка",
            ),
        ),
    ]
