# Generated by Django 2.2.10 on 2020-05-04 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_auto_20200504_0957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='property',
            options={'get_latest_by': ['created'], 'ordering': ['-created'], 'verbose_name_plural': 'properties'},
        ),
    ]