# Generated by Django 2.2.10 on 2020-07-12 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_auto_20200711_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faq', to='hotels.Hotel'),
        ),
    ]
