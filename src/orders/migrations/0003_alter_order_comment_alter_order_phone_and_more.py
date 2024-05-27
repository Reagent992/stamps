# Generated by Django 4.2.11 on 2024-04-11 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_rename_text_order_stamp_text_order_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.TextField(
                blank=True, default="", verbose_name="Комментарий"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.CharField(
                max_length=20,
                validators=[django.core.validators.MinLengthValidator(6)],
                verbose_name="Телефон",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="postal_code",
            field=models.CharField(
                blank=True,
                default="",
                max_length=20,
                verbose_name="Почтовый индекс",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="stamp_text",
            field=models.JSONField(
                blank=True, verbose_name="Содержание печати"
            ),
        ),
    ]