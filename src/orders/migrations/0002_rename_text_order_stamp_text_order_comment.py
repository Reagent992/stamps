# Generated by Django 4.2.8 on 2024-02-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="text",
            new_name="stamp_text",
        ),
        migrations.AddField(
            model_name="order",
            name="comment",
            field=models.TextField(
                blank=True, null=True, verbose_name="Комментарий"
            ),
        ),
    ]
