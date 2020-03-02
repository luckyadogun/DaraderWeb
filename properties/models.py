from django.db import models
from django.utils.translation import gettext as _


class Country(models.Model):
    name = models.CharField(_("country name"), max_length=200)

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(_("state name"), max_length=200)


class Property(models.Model):
    PROPERTY_STATUS = (
        ("sale", "sale"),
        ("rent", "rent"),
        ("lease", "lease"),
    )

    PROPERTY_TYPE = (
        ("all", "all"),
        ("flat", "flat"),
        ("house", "house"),
        ("land", "land"),
        ("commercial", "commercial"),
        ("event centre", "event centre"),
    )

    title = models.CharField(_("title"), max_length=200)
    address = models.CharField(_("address"), max_length=200)
    neighborhood = models.CharField(_("neighborhood"), max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    zipcode = models.CharField(_("zipcode or postal code"), max_length=20, blank=True, null=True)
    property_status = models.CharField(_("status"), max_length=20, default="rent")
    property_type = models.CharField(_("type"), max_length=20, default="all")
    