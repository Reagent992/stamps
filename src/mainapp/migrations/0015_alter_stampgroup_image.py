# Generated by Django 4.2.14 on 2024-07-21 17:21

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0014_alter_stamp_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stampgroup",
            name="image",
            field=models.ImageField(
                help_text="Загрузить картинку",
                upload_to=core.utils.get_renamed_image_path,
                verbose_name="Картинка",
            ),
        ),
    ]
