from django import template

from properties.models import Property

register = template.Library()


@register.simple_tag
def total_properties(user=None):
    if user:
        return Property.objects.filter(
            owner__manager=user).count()
    return Property.objects.count()
