from django.db import models
from django.utils.translation import gettext as _
from users.utils import validate_phone
from properties.models import TimeStampedModel
from users.models import User


class Hotel(TimeStampedModel):
    HOTEL_TYPE_CHOICES = (
        ("Hotel", "Hotel"),
        ("Motel", "Motel"),
        ("Inn", "Inn")
    )

    name = models.CharField(_("name"), max_length=200, unique=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(_("address"))
    hotel_type = models.CharField(
        _("hotel type"), max_length=200, 
        choices=HOTEL_TYPE_CHOICES, blank=True)
    number_of_rooms = models.IntegerField(_("number of rooms"))
    description = models.TextField(_("description"))
    has_restaurant = models.BooleanField(_("restaurant"), default=False)
    has_bar = models.BooleanField(_("bar"), default=False)
    has_wireless_internet = models.BooleanField(
        _("wireless internet"), default=False)
    has_24_hrs_electricity = models.BooleanField(
        _("24 hrs electricity"), default=False)
    has_adequate_parking_space = models.BooleanField(
        _("adequate parking space"), default=False)
    has_swimming_pool = models.BooleanField(_("swimming pool"), default=False)
    has_car_rental = models.BooleanField(_("car rental"), default=False)
    has_double_bed = models.BooleanField(_("double bed"), default=False)
    has_toiletries = models.BooleanField(_("toiletries"), default=False)
    has_concierge = models.BooleanField(_("concierge"), default=False)
    has_shower = models.BooleanField(_("shower"), default=False)
    has_room_service = models.BooleanField(_("room service"), default=False)
    has_key_card_system = models.BooleanField(
        _("key card system"), default=False)
    has_gym = models.BooleanField(_("gym"), default=False)
    has_airport_pickup = models.BooleanField(
        _("airport pickup"), default=False)
    has_car_hire = models.BooleanField(_("car hire"), default=False)
    has_laundry = models.BooleanField(_("laundry"), default=False)
    has_spa_treatment = models.BooleanField(_("spa treatment"), default=False)
    has_night_club = models.BooleanField(_("night club"), default=False)
    has_luggage_storage = models.BooleanField(
        _("luggage storage"), default=False)
    has_air_conditioning = models.BooleanField(
        _("air conditioning"), default=False)
    has_car_wash = models.BooleanField(_("car wash"), default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


def hotel_photos_image_path(instance, filename):
    return f"hotels/{instance.hotel.name}/images/{filename}"


class HotelPhotos(models.Model):
    photo = models.ImageField(
        _("image"), upload_to=hotel_photos_image_path, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotelPhotos")


class Room(models.Model):
    room_name = models.CharField(_("room name"), max_length=200)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    information = models.TextField(_("room information"))
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="room")

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name_plural = "Rooms"


class FAQ(models.Model):
    question = models.CharField(_("question"), max_length=200)
    answer = models.CharField(_("answer"), max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="faq")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQs"

class HotelBookingRequest(TimeStampedModel):
    BOOKED = "booked"
    UNBOOKED = "unbooked"

    BOOKING_STATUS = (
        (BOOKED, BOOKED),
        (UNBOOKED, UNBOOKED),
    )

    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, null=True, default=UNBOOKED, choices=BOOKING_STATUS)
    client = models.ForeignKey(
        User, on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE)
    mobile_phone = models.CharField(
        validators=[validate_phone], max_length=17, null=True, blank=True)


class BookmarkedHotel(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarkedHotel')
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='bookmarkedHotel')