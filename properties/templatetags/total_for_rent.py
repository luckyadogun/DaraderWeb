from django import template

from properties.models import Property

register = template.Library()


@register.simple_tag
def total_for_rent(user=None):
    if user:
        Property.objects.filter(
            owner__manager=user,
            property_category="rent").count()
    return Property.forrent.count()