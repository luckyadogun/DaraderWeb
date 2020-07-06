from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

# Create your models here.
def hotel_photos_image_path(instance, filename):
    return f"hotels/{instance.name}/images/{filename}"

class Hotel(models.Model):
    HOTEL_TYPE_CHOICES = (
        ("Hotel", "Hotel"),
    )
    name = models.CharField(_("company name"), max_length=200, unique=True)
    photos = ArrayField(models.ImageField(_("photos"), upload_to=hotel_photos_image_path, null=True, blank=True))
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(_("address"))
    hotel_information = ArrayField(models.CharField(_("hotel information"), max_length=200))
    rooms = models.ManyToManyField()
    hotel_type = models.CharField(_("hotel type"), choices=HOTEL_TYPE_CHOICES, blank=True)
    number_of_rooms = models.IntegerField(_("number of rooms"))
    description = models.TextField(_("description"))
    terms_and_conditions = models.CharField(_("terms and conditions"))

    def __str__(self):
        return self.name

class Room(models.Model):
    # Standard, Deluxe, Double Deluxe, Executive Suite
    room_name = models.CharField(_("room name"), max_length=200)
    price = models.DecimalField(_("price"),max_digits=10, decimal_places=2)
    information = models.TextField(_("room information"))
    facilities = ArrayField(models.CharField(_("facilities"), max_length=200))
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(_("question"), max_length=200)
    answer = models.CharField(_("answer"), max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question