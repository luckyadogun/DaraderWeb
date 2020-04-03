from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.deprecation import MiddlewareMixin

from properties.models import Property


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["recent_properties"] = Property.objects.order_by("created")[:3]

        return context


class MyPropertyView(TemplateView):
    template_name = "users/my_properties.html"


class MyBookingsView(TemplateView):
    template_name = "users/my_bookings.html"


class AddPropertyView(TemplateView):
    template_name = "users/add_property.html"


class MyAccountView(TemplateView):
    template_name = "users/my_account.html"


class UpdateAccountView(TemplateView):
    template_name = "users/update_account.html"


class BookmarkedView(TemplateView):
    template_name = "users/bookmarks.html"