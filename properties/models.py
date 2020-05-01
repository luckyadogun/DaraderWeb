from django.utils.crypto import get_random_string
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from users.models import User
from users.utils import validate_phone

from .managers import PropertyForSaleManager, \
    PropertyForRentManager, PropertyForLeaseManager, \
    ApprovedAgentManager, ApprovedDeveloperManager, \
    FeaturedCompaniesManager


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ''created'' and ''modified'' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(_("country"), max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"


class State(models.Model):
    name = models.CharField(_("state"), max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class LGA(models.Model):
    name = models.CharField(_("LGA"), max_length=200)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LGA"
        verbose_name_plural = "LGA"


def company_logo_image_path(instance, filename):
    return f"companies/{instance.name}/images/{filename}"


class Company(TimeStampedModel):
    ESTATE_AGENT = "agent"
    PROPERTY_DEVELOPER = "developer"

    ACCOUNT_TYPE_CHOICES = (
        (ESTATE_AGENT, ESTATE_AGENT),
        (PROPERTY_DEVELOPER, PROPERTY_DEVELOPER)
    )

    is_approved = models.BooleanField(
        _("approve company"),
        help_text="click here to approve or disapprove this company",
        default=False)
    is_featured = models.BooleanField(
        _("feature company"),
        help_text="click here if this company made payment to be featured",
        default=False)
    is_featured_expires = models.DateField(
        null=True, verbose_name="feature expiry date", blank=True)
    manager = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="company")
    name = models.CharField(
        _("company name"), max_length=200, unique=True)    
    office_phone = models.CharField(
        validators=[validate_phone], max_length=17,
        null=True, blank=True)
    mobile_phone = models.CharField(
        validators=[validate_phone], max_length=17,
        null=True, blank=True)
    address = models.CharField(_("address"), max_length=200, null=True)
    about = models.TextField(_("about"), blank=True, null=True)
    logo = models.ImageField(
        _("logo"), upload_to=company_logo_image_path,
        default='', null=True, blank=True)
    account_type = models.CharField(
        _("account type"), max_length=20, 
        choices=ACCOUNT_TYPE_CHOICES, default=ESTATE_AGENT)

    objects = models.Manager()
    agents = ApprovedAgentManager()
    developers = ApprovedDeveloperManager()
    featured = FeaturedCompaniesManager()

    def get_absolute_url(self):
        return reverse(
            f"companies/{self.account_type.lower()}/{self.name}/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"


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

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"

    PROPERTY_CATEGORY_CHOICES = (
        (SALE, SALE),
        (RENT, RENT),
        (LEASE, LEASE),
    )

    PROPERTY_TYPE_CHOICES = (
        (ALL, ALL),
        (FLAT, FLAT),
        (HOUSE, HOUSE),
        (LAND, LAND),
        (COMMERCIAL, COMMERCIAL),
        (EVENT_CENTRE, EVENT_CENTRE),
    )

    PROPERTY_MARKET_STATUS = (
        (AVAILABLE, AVAILABLE),
        (UNAVAILABLE, UNAVAILABLE)
    )

    property_id = models.CharField(
        _("Property ID"), max_length=40, unique=True, 
        default=get_random_string)
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=400, blank=True)
    address = models.CharField(_("address"), max_length=200)
    lga = models.ForeignKey(
        LGA, on_delete=models.SET_NULL,
        null=True, default='', related_name='property_lga')
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL,
        null=True, default='')
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL,
        null=True, related_name='property_state')
    zipcode = models.CharField(
        _("zipcode or postal code"),
        max_length=20, blank=True, null=True)
    property_category = models.CharField(
        _("category"), max_length=20, 
        choices=PROPERTY_CATEGORY_CHOICES,
        default=SALE)
    property_type = models.CharField(
        _("type"), max_length=20, default=ALL,
        choices=PROPERTY_TYPE_CHOICES)
    market_status = models.CharField(
        _("status"), max_length=20, 
        choices=PROPERTY_MARKET_STATUS,
        default=AVAILABLE)
    price = models.DecimalField(
        _("price"), 
        max_digits=20, decimal_places=2)
    owner = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="property")
    description = models.TextField(_("description"), null=True, blank=True)

    objects = models.Manager()
    forsale = PropertyForSaleManager()
    forrent = PropertyForRentManager()
    forlease = PropertyForLeaseManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Property, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/property/{self.pk}/{self.slug}/"

    def __str__(self):
        return f"#{self.property_id} - {self.title}"

    class Meta:
        verbose_name_plural = "properties"
        get_latest_by = ["created"]


def property_images_directory_path(instance, filename):
    return f"property/{instance.property_obj.property_id}/images/{filename}"


class Gallery(models.Model):
    image = models.ImageField(
        _("image"), upload_to=property_images_directory_path, blank=True)
    property_obj = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="gallery")

    class Meta:
        verbose_name_plural = "gallery"


class PropertyDetails(models.Model):
    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    livingrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    bathrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveSmallIntegerField(blank=True, null=True)
    total_area = models.PositiveSmallIntegerField(blank=True, null=True)
    covered_area = models.PositiveSmallIntegerField(blank=True, null=True)
    toilets = models.PositiveSmallIntegerField(blank=True, null=True)
    has_basketball_court = models.BooleanField(
        _("basketball court"), default=False)
    has_gym = models.BooleanField(
        _("gym"), default=False)
    is_wheelchair_friendly = models.BooleanField(
        _("wheelchair friendly"), default=False)
    has_swimming_pool = models.BooleanField(
        _("swimming pool"), default=False)
    property_obj = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="property_details")

    class Meta:
        verbose_name_plural = "Property Details"


class BookingRequest(TimeStampedModel):
    BOOKED = "booked"
    UNBOOKED = "unbooked"

    BOOKING_STATUS = (
        (BOOKED, BOOKED),
        (UNBOOKED, UNBOOKED),
    )

    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, null=True, default=UNBOOKED, choices=BOOKING_STATUS)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="bookingrequest")
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookingrequest")
    property_details = models.ForeignKey(
        PropertyDetails, on_delete=models.CASCADE,
        related_name="bookingrequest")
    mobile_phone = models.CharField(
        validators=[validate_phone], max_length=17, null=True, blank=True)


class BookmarkedProperty(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    property_obj = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="bookmarked")
