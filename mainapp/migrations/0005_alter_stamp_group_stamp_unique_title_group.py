# Generated by Django 4.2.3 on 2023-07-29 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_group_options_remove_group_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stamp',
            name='group',
            field=models.ForeignKey(help_text='Группа, к которой будет относиться штамп', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='stamps', to='mainapp.group', verbose_name='Группа'),
        ),
        migrations.AddConstraint(
            model_name='stamp',
            constraint=models.UniqueConstraint(fields=('title', 'group'), name='unique_title_group'),
        ),
    ]
