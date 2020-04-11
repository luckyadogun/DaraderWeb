from django import template

from properties.models import BookmarkedProperty as Bookmarked

register = template.Library()


@register.simple_tag
def total_bookmarks(user):
    return Bookmarked.objects.filter(
        owner=user).count()
