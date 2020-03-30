from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.contrib.auth import login, logout, authenticate


class LoginView(View):
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            username=username,
            password=password
            )
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(
                    reverse("dashboard")
                )


class DashboardView(TemplateView):
    template_name = "users/index.html"


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