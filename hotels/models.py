from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Hotel(models.Model):
    HOTEL_TYPE_CHOICES = (
        ("Hotel", "Hotel"),
    )
    name = models.CharField(_("company name"), max_length=200, unique=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(_("address"))
    rooms = models.ManyToManyField('Room')
    hotel_type = models.CharField(_("hotel type"), choices=HOTEL_TYPE_CHOICES, blank=True)
    number_of_rooms = models.IntegerField(_("number of rooms"))
    description = models.TextField(_("description"))

    def __str__(self):
        return self.name

def hotel_photos_image_path(instance, filename):
    return f"hotels/{instance.hotel.name}/images/{filename}"

class HotelPhotos(models.Model):
    photo = models.ImageField(_("image"), upload_to=hotel_photos_image_path, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

class Room(models.Model):
    # Standard, Deluxe, Double Deluxe, Executive Suite
    room_name = models.CharField(_("room name"), max_length=200)
    price = models.DecimalField(_("price"),max_digits=10, decimal_places=2)
    information = models.TextField(_("room information"))

    def __str__(self):
        return self.room_name

class Facility(models.Model):
    # Restaurant, Bars/Lounge, Wireless Internet, Electricity, Adequate Parking, Adequate Parking Space, Swimming pool,
    facility_name = models.CharField(_("facility name"), max_length=200)
    hotel = models.ManyToManyField(Hotel)

    def __str__(self):
        return self.facility_name

class FAQ(models.Model):
    question = models.CharField(_("question"), max_length=200)
    answer = models.CharField(_("answer"), max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question