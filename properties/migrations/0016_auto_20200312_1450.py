# Generated by Django 2.2.10 on 2020-03-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0015_auto_20200312_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(default='a14746be', max_length=8, unique=True, verbose_name='Property ID'),
        ),
    ]
