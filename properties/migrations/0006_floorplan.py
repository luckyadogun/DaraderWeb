# Generated by Django 2.2.10 on 2020-05-02 18:22

from django.db import migrations, models
import django.db.models.deletion
import properties.models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_auto_20200501_0846'),
    ]

    operations = [
        migrations.CreateModel(
            name='FloorPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='title: eg - first floor')),
                ('size', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='size: (in square foot)')),
                ('rooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='room size: (in square foot)')),
                ('bathrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='bathroom size: (in square foot)')),
                ('image', models.ImageField(blank=True, upload_to=properties.models.property_images_directory_path, verbose_name='image')),
                ('property_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floorplan', to='properties.Property')),
            ],
            options={
                'verbose_name_plural': 'Floor Plan',
            },
        ),
    ]
