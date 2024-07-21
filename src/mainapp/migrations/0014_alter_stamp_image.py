# Generated by Django 4.2.14 on 2024-07-21 13:15

import core.abstract_models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0013_alter_stamp_form_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stamp",
            name="image",
            field=models.ImageField(
                upload_to=core.abstract_models.get_renamed_image_path,
                verbose_name="Картинка",
            ),
        ),
    ]
