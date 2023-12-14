# Generated by Django 4.2.6 on 2023-12-14 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("printy", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StampGroup",
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
                    "title",
                    models.CharField(
                        help_text="Название группы",
                        max_length=200,
                        unique=True,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Уникальный текстовый идентификатор группы",
                        unique=True,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Загрузить картинку",
                        upload_to="",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        help_text="Включение и выключение отображения на сайте",
                        verbose_name="Опубликованно",
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
                    "min_group_price",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Минимальная цена"
                    ),
                ),
            ],
            options={
                "verbose_name": "Группа печатей",
                "verbose_name_plural": "Группы печатей",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Stamp",
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
                    "title",
                    models.CharField(max_length=200, verbose_name="Заголовок"),
                ),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(verbose_name="Описание")),
                ("price", models.PositiveIntegerField(verbose_name="Цена")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        help_text="Включение и выключение отображение на сайте",
                        verbose_name="Опубликованно",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="", verbose_name="Картинка"),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="stamps",
                        to="mainapp.stampgroup",
                        verbose_name="Группа",
                    ),
                ),
                (
                    "printy",
                    models.ManyToManyField(
                        error_messages="Печать должна быть привязанна хотя бы к одной оснастке.",
                        related_name="printy",
                        to="printy.printy",
                        verbose_name="Оснастка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Печать",
                "verbose_name_plural": "Печати",
                "ordering": ("-created",),
            },
        ),
        migrations.AddConstraint(
            model_name="stamp",
            constraint=models.UniqueConstraint(
                fields=("title", "group"), name="unique_title_group"
            ),
        ),
    ]
