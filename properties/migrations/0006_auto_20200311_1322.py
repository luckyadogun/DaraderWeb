# Generated by Django 2.2.10 on 2020-03-11 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_auto_20200311_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(default='c6584faf', max_length=8, unique=True, verbose_name='Property ID'),
        ),
    ]