# Generated by Django 2.2.10 on 2020-05-04 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_auto_20200504_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floorplan',
            name='title',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='title: eg - first floor'),
        ),
    ]
