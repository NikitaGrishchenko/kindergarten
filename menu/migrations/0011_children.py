# Generated by Django 3.1.7 on 2021-04-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_auto_20210405_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('young', models.IntegerField(verbose_name='Количество детей в яслях')),
                ('old', models.IntegerField(verbose_name='Количество детей в старшей группе')),
            ],
            options={
                'verbose_name': 'Количество детей',
            },
        ),
    ]