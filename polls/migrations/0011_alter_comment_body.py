# Generated by Django 3.2.5 on 2021-08-21 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_alter_comment_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=80, verbose_name='Оставьте комментарий'),
        ),
    ]
