from django.db import models


class ApprovedAgentManager(models.Manager):
    """
        Property manager to get all
        approved estate agents.

        __model__ = Companies
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            is_approved=True, account_type="agent"
        )


class ApprovedDeveloperManager(models.Manager):
    """
        Property manager to get all
        approved property developers.

        __model__ = Companies
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            is_approved=True, account_type="developer"
        )


class FeaturedCompaniesManager(models.Manager):
    """
        Property manager to get all
        featured properties.

        __model__ = Companies
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            is_featured=True
        )


class PropertyForSaleManager(models.Manager):
    """
        Property manager to get all
        properties listed for sale.

        __model__ = Properties
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            property_category="sale"
        )


class PropertyForRentManager(models.Manager):
    """
        Property manager to get all
        properties listed for rent.

        __model__ = Properties
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            property_category="rent"
        )


class PropertyForLeaseManager(models.Manager):
    """
        Property manager to get all
        properties listed for lease.

        __model__ = Properties
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            property_category="lease"
        )
