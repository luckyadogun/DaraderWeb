# Generated by Django 2.2.10 on 2020-04-17 08:11

from django.db import migrations, models
import properties.models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_auto_20200416_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(blank=True, upload_to=properties.models.property_images_directory_path, verbose_name='image'),
        ),
    ]
