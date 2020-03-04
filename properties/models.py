import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from users.models import User

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


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(_("state"), max_length=200)


def company_logo_image_path(instance, filename):
    return f"companies/{instance.id}/images/{filename}"


class Company(TimeStampedModel):
    ESTATE_AGENT = "agent"
    PROPERTY_DEVELOPER = "developer"

    ACCOUNT_TYPE_CHOICES = (
        (ESTATE_AGENT, ESTATE_AGENT),
        (PROPERTY_DEVELOPER, PROPERTY_DEVELOPER)
    )

    is_approved = models.BooleanField(
        _("approved companies"), 
        help_text="click here to approve or disapprove this company", 
        default=False)
    is_featured = models.BooleanField(
        _("featured companies"), 
        help_text="click here if this company made payment to be featured", 
        default=False)
    is_featured_expires = models.DateField(null=True)
    manager = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(
        _("company name"), max_length=200, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the "
                "format: '+999999999'. Up to 15 digits allowed.")
    office_phone = models.CharField(validators=[phone_regex], max_length=17)
    mobile_phone = models.CharField(validators=[phone_regex], max_length=17)
    about = models.TextField(_("about"), blank=True, null=True)
    logo = models.ImageField(
        _("logo"), upload_to=company_logo_image_path, default='')
    account_type = models.CharField(
        _("account type"), max_length=20, choices=ACCOUNT_TYPE_CHOICES)

    agents = ApprovedAgentManager()
    developers = ApprovedDeveloperManager()
    featured = FeaturedCompaniesManager()

    def get_absolute_url(self):
        return reverse(
            f"company-detail/{self.account_type.lower()}", 
            kwargs={'id': self.pk})

    def __str__(self):
        return self.name


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
        max_length=8, unique=True, default=uuid.uuid4().hex[8:16])
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
    property_category = models.CharField(
        _("category"), max_length=20, 
        choices=PROPERTY_CATEGORY_CHOICES)
    property_type = models.CharField(
        _("type"), max_length=20, 
        choices=PROPERTY_TYPE_CHOICES)
    market_status = models.CharField(
        _("status"), max_length=20, 
        choices=PROPERTY_MARKET_STATUS)
    price = models.DecimalField(
        _("price"), 
        max_digits=20, decimal_places=2)
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField(_("description"))

    objects = models.Manager()
    forsale = PropertyForSaleManager()
    forrent = PropertyForRentManager()
    forlease = PropertyForLeaseManager()

    def __str__(self):
        return f"#{self.property_id} - {self.title}"

    class Meta:
        get_latest_by = ["created"]


def property_images_directory_path(instance, filename):
    return f"property/{instance.property_id}/images/{filename}"


class Gallery(models.Model):
    image = models.ImageField(
        _("image"), upload_to=property_images_directory_path)
    video_link = models.URLField(max_length=255)
    property_obj = models.ForeignKey(Property, on_delete=models.CASCADE)


class PropertyDetails(models.Model):
    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    livingrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    bathrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveSmallIntegerField(blank=True, null=True)
    total_area = models.PositiveSmallIntegerField(blank=True, null=True)
    covered_area = models.PositiveSmallIntegerField(blank=True, null=True)
    toilets = models.PositiveSmallIntegerField(blank=True, null=True)
    has_basketball_court = models.BooleanField(
        _("basketball court"), blank=True, null=True)
    has_gym = models.BooleanField(
        _("gym"), blank=True, null=True)
    is_wheelchair_friendly = models.BooleanField(
        _("wheelchair friendly"), blank=True, null=True)
    has_swimming_pool = models.BooleanField(
        _("swimming pool"), blank=True, null=True)
    property_obj = models.ForeignKey(Property, on_delete=models.CASCADE)