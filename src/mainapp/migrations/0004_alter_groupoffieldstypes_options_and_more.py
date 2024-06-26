# Generated by Django 4.2.8 on 2023-12-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0003_alter_fieldstypes_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="groupoffieldstypes",
            options={
                "ordering": ("-created",),
                "verbose_name": "Группа типов полей",
                "verbose_name_plural": "Группы типов полей",
            },
        ),
        migrations.AddField(
            model_name="groupoffieldstypes",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата создания"
            ),
            preserve_default=False,
        ),
    ]
