# Generated by Django 3.1.7 on 2021-04-05 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_auto_20210405_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productindish',
            old_name='dish_and_product',
            new_name='dish',
        ),
    ]