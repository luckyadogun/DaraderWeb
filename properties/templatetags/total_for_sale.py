from django import template

from properties.models import Property

register = template.Library()


@register.simple_tag
def total_for_sale(user=None):
    if user:
        Property.objects.filter(
            owner__manager=user,
            property_category="sale").count()
    return Property.forsale.count()