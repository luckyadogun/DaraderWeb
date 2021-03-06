# Generated by Django 2.2.10 on 2020-07-07 15:16

from django.db import migrations, models
import django.db.models.deletion
import hotels.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='company name')),
                ('average_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.TextField(verbose_name='address')),
                ('hotel_type', models.CharField(blank=True, choices=[('Hotel', 'Hotel')], max_length=200, verbose_name='hotel type')),
                ('number_of_rooms', models.IntegerField(verbose_name='number of rooms')),
                ('description', models.TextField(verbose_name='description')),
                ('has_restaurant', models.BooleanField(default=False, verbose_name='restaurant')),
                ('has_bar', models.BooleanField(default=False, verbose_name='bar')),
                ('has_wireless_internet', models.BooleanField(default=False, verbose_name='wireless internet')),
                ('has_24_hrs_electricity', models.BooleanField(default=False, verbose_name='24 hrs electricity')),
                ('has_adequate_parking_space', models.BooleanField(default=False, verbose_name='adequate parking space')),
                ('has_swimming_pool', models.BooleanField(default=False, verbose_name='swimming pool')),
                ('has_car_rental', models.BooleanField(default=False, verbose_name='car rental')),
                ('has_double_bed', models.BooleanField(default=False, verbose_name='double bed')),
                ('has_toiletries', models.BooleanField(default=False, verbose_name='toiletries')),
                ('has_concierge', models.BooleanField(default=False, verbose_name='concierge')),
                ('has_shower', models.BooleanField(default=False, verbose_name='shower')),
                ('has_room_service', models.BooleanField(default=False, verbose_name='room service')),
                ('has_key_card_system', models.BooleanField(default=False, verbose_name='key card system')),
                ('has_gym', models.BooleanField(default=False, verbose_name='gym')),
                ('has_airport_pickup', models.BooleanField(default=False, verbose_name='airport pickup')),
                ('has_car_hire', models.BooleanField(default=False, verbose_name='car hire')),
                ('has_laundry', models.BooleanField(default=False, verbose_name='laundry')),
                ('has_spa_treatment', models.BooleanField(default=False, verbose_name='spa treatment')),
                ('has_night_club', models.BooleanField(default=False, verbose_name='night club')),
                ('has_luggage_storage', models.BooleanField(default=False, verbose_name='luggage storage')),
                ('has_air_condititoning', models.BooleanField(default=False, verbose_name='air conditioning')),
                ('has_car_wash', models.BooleanField(default=False, verbose_name='car wash')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=200, verbose_name='room name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('information', models.TextField(verbose_name='room information')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HotelPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to=hotels.models.hotel_photos_image_path, verbose_name='image')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='question')),
                ('answer', models.CharField(max_length=200, verbose_name='answer')),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotel')),
            ],
        ),
    ]
