from django.urls import reverse
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.deprecation import MiddlewareMixin

from properties.models import Property, Company, BookingRequest


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, *args, **kwargs):
        property_obj = Property.objects.filter(
            owner__manager=self.request.user)

        context = super().get_context_data(**kwargs)
        context["my_properties_count"] = property_obj.count()
        context["my_properties_forsale"] = property_obj.filter(
            property_category="sale").count()
        context["my_properties_forrent"] = property_obj.filter(
            property_category="rent").count()
        context["recent_properties"] = property_obj.order_by("created")[:3]

        return context


class MyPropertyView(LoginRequiredMixin, ListView):
    template_name = "users/my_properties.html"
    context_object_name = "properties"
    paginate_by = 5

    def get_queryset(self):
        company = Company.objects.get(manager=self.request.user)
        return Property.objects.filter(owner=company)


@login_required
def property_delete_view(request):
    company = get_object_or_404(Company, manager=request.user)

    if request.is_ajax and request.method == "POST":
        property_id = request.POST.get("propertyID")
        property_obj = get_object_or_404(Property, id=property_id)

        if property_obj.owner == company:
            property_obj.delete()
            return JsonResponse({"result": "Success!"})
        return JsonResponse({"result": "Unauthorized Access!"})

    return redirect(reverse("users:my-properties"))


class MyBookingsView(LoginRequiredMixin, ListView):
    template_name = "users/my_bookings.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):        
        return BookingRequest.objects.filter(
            company__manager=self.request.user,
            status="booked")


@login_required
def booking_delete_view(request):
    company = get_object_or_404(Company, manager=request.user)

    if request.is_ajax and request.method == "POST":
        booking_id = request.POST.get("bookingID")
        booking = get_object_or_404(BookingRequest, id=booking_id)

        if booking.company == company:
            booking.delete()
            return JsonResponse({"result": "Success!"})
        return JsonResponse({"result": "Unauthorized Access!"})

    return redirect(reverse("users:my-bookings"))


@login_required
def booking_setup_view(request):
    if request.is_ajax and request.method == "POST":
        booking_id = request.POST.get("bookingID")
        booking = get_object_or_404(BookingRequest, id=booking_id)
        # send email
        booking.status = "unbooked"
        booking.save()
        return JsonResponse({"result": "Success!"})

    return redirect(reverse("users:my-bookings"))


class AddPropertyView(LoginRequiredMixin, TemplateView):
    template_name = "users/add_property.html"


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/my_account.html"


class UpdateAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/update_account.html"


class BookmarkedView(LoginRequiredMixin, TemplateView):
    template_name = "users/bookmarks.html"