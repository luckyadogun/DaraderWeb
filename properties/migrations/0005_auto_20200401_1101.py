# Generated by Django 2.2.10 on 2020-04-01 11:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_auto_20200325_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(default=uuid.UUID('fd731f55-5a6d-4f49-9fe4-472c2cf98ced'), max_length=40, unique=True, verbose_name='Property ID'),
        ),
    ]
