import random

from .models import Company


def get_currently_featured():
    """
    Here we use randomly select a featured
    company and list their property on the
    `HomePageView`

    """
    featured_companies = Company.objects.filter(
        is_approved=True, is_featured=True)
    total_featured_companies = featured_companies.count()
    try:
        currently_featured = featured_companies[
            random.randrange(0, total_featured_companies)]
        return currently_featured.property.all()[:5]
    except ValueError:
        return Company.objects.filter(is_approved=True)[:5]
