# Generated by Django 2.2.10 on 2020-03-11 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_auto_20200311_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(default='359e41a0', max_length=8, unique=True, verbose_name='Property ID'),
        ),
    ]
