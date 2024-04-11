# Generated by Django 4.2.8 on 2024-02-11 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("printy", "0002_alter_printy_group_alter_printy_published_and_more"),
        ("mainapp", "0008_alter_fieldstypes_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="email"),
                ),
                (
                    "phone",
                    models.CharField(max_length=20, verbose_name="phone"),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Полное имя"
                    ),
                ),
                (
                    "address",
                    models.CharField(max_length=200, verbose_name="Адрес"),
                ),
                (
                    "city",
                    models.CharField(max_length=100, verbose_name="Город"),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Почтовый индекс",
                    ),
                ),
                ("text", models.TextField(verbose_name="Содержание печати")),
                (
                    "printy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="printy.printy",
                        verbose_name="Оснастка",
                    ),
                ),
                (
                    "stamp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="mainapp.stamp",
                        verbose_name="Печать",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
            },
        ),
    ]
