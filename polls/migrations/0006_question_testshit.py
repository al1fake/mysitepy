# Generated by Django 3.2.5 on 2021-08-04 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20210805_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='testshit',
            field=models.TextField(default='lol'),
            preserve_default=False,
        ),
    ]