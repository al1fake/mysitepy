# Generated by Django 3.2.7 on 2021-09-14 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20210914_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='userid',
            field=models.IntegerField(default=1),
        ),
    ]
