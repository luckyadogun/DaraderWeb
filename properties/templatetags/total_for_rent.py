from django import template

from properties.models import Property

register = template.Library()


@register.simple_tag
def total_for_rent():
    return Property.forrent.count()