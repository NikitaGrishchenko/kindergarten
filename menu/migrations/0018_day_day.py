# Generated by Django 3.1.7 on 2021-04-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0017_auto_20210418_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='day',
            field=models.DateField(blank=True, null=True, verbose_name='Дата'),
        ),
    ]
