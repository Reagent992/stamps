# Generated by Django 4.2.8 on 2024-02-10 20:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "mainapp",
            "0006_fieldstypes_updated_alter_fieldstypes_help_text_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fieldstypes",
            options={
                "ordering": ("-updated",),
                "verbose_name": "Тип поля формы",
                "verbose_name_plural": "Типы полей формы",
            },
        ),
        migrations.AlterModelOptions(
            name="groupoffieldstypes",
            options={
                "ordering": ("-updated",),
                "verbose_name": "Группа типов полей",
                "verbose_name_plural": "Группы типов полей",
            },
        ),
        migrations.AddField(
            model_name="groupoffieldstypes",
            name="updated",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Дата последнего изменения"
            ),
        ),
    ]
