# Generated by Django 2.2.10 on 2020-04-30 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20200430_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='lga',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_lga', to='properties.LGA'),
        ),
    ]
