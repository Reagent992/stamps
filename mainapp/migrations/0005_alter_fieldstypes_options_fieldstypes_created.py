# Generated by Django 4.2.8 on 2023-12-27 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0004_alter_groupoffieldstypes_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fieldstypes",
            options={
                "ordering": ("-created",),
                "verbose_name": "Тип поля формы",
                "verbose_name_plural": "Типы полей формы",
            },
        ),
        migrations.AddField(
            model_name="fieldstypes",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата создания",
            ),
            preserve_default=False,
        ),
    ]
