# Generated by Django 3.1.7 on 2021-04-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0020_auto_20210418_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='count_person',
            field=models.IntegerField(default=20, verbose_name='Количество детей'),
        ),
    ]