# Generated by Django 2.2.10 on 2020-07-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_auto_20200712_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_type',
            field=models.CharField(blank=True, choices=[('Hotel', 'Hotel'), ('Motel', 'Motel'), ('Inn', 'Inn')], max_length=200, verbose_name='hotel type'),
        ),
    ]