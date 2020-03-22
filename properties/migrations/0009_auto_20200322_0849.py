# Generated by Django 2.2.10 on 2020-03-22 08:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_auto_20200322_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(default=uuid.UUID('b56cc564-3f04-4a4c-8b34-4f3f82142d6e'), max_length=40, unique=True, verbose_name='Property ID'),
        ),
    ]
