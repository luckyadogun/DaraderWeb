from django.db import models
from django.utils.translation import gettext as _

from users.models import Agent
from users.abstract import TimeStampedModel


def property_directory_path(instance, filename):
    return f"property/{instance.property_id}/images/{filename}"


class Country(models.Model):
    name = models.CharField(_("country name"), max_length=200)

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(_("state name"), max_length=200)


class Property(TimeStampedModel):
    SALE = "sale"
    RENT = "rent"
    LEASE = "lease"

    ALL = "all"
    FLAT = "flat"
    HOUSE = "house"
    LAND = "land"
    COMMERCIAL = "commercial"
    EVENT_CENTRE = "event centre"

    PROPERTY_STATUS_CHOICES = (
        (SALE, "sale"),
        (RENT, "rent"),
        (LEASE, "lease"),
    )

    PROPERTY_TYPE_CHOICES = (
        (ALL, "all"),
        (FLAT, "flat"),
        (HOUSE, "house"),
        (LAND, "land"),
        (COMMERCIAL, "commercial"),
        (EVENT_CENTRE, "event centre"),
    )

    property_id = models.CharField(max_length=7, unique=True)
    title = models.CharField(_("title"), max_length=200)
    address = models.CharField(_("address"), max_length=200)
    neighborhood = models.CharField(
        _("neighborhood"), max_length=200, 
        blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    zipcode = models.CharField(
        _("zipcode or postal code"), 
        max_length=20, blank=True, null=True)
    property_status = models.CharField(
        _("status"), max_length=20, 
        choices=PROPERTY_STATUS_CHOICES)
    property_type = models.CharField(
        _("type"), max_length=20, 
        choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(
        _("property price"), 
        max_digits=20, decimal_places=2)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    description = models.TextField(_("description"))

    def _get_property(self):
        return f"#{self.property_id} - {self.title} - {self.agent.company_name}"

    def __str__(self):
        return self._get_property()

    ordering = ["created"]


class Gallery(models.Model):
    image = models.ImageField(_("image"), upload_to=property_directory_path)
    video_link = models.URLField(max_length=255)
    property_obj = models.ForeignKey(Property, on_delete=models.CASCADE)


class PropertyDetails(models.Model):
    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    livingrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    baths = models.PositiveSmallIntegerField(blank=True, null=True)
    garages = models.PositiveSmallIntegerField(blank=True, null=True)
    has_basketball_court = models.BooleanField(
        _("basketball court"), blank=True, null=True)
    has_gym = models.BooleanField(
        _("gym"), blank=True, null=True)
    is_wheelchair_friendly = models.BooleanField(
        _("wheelchair friendly"), blank=True, null=True)
    has_swimming_pool = models.BooleanField(
        _("swimming pool"), blank=True, null=True)
    property_obj = models.ForeignKey(Property, on_delete=models.CASCADE)
