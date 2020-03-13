# Generated by Django 2.2.10 on 2020-03-13 09:23

from django.db import migrations, models
import django_resized.forms
import properties.models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0016_auto_20200312_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=0, size=[1280, 960], upload_to=properties.models.property_images_directory_path),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(default='91a14505', max_length=8, unique=True, verbose_name='Property ID'),
        ),
    ]
