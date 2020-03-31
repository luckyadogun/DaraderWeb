from django.views.generic.base import TemplateView


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