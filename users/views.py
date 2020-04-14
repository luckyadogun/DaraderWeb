from django.views.generic import ListView
from django.shortcuts import (
            get_object_or_404, render,
            redirect, reverse)
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    PropertyForm,
    GalleryForm,
    PropertyDetailsForm)

from properties.models import (
    Property, Company,
    BookingRequest, 
    BookmarkedProperty)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_properties"] = Property.objects.order_by("created")[:3]

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

    raise Http404("Page Doesn't Exist!")


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

    raise Http404("Page Doesn't Exist!")


@login_required
def booking_setup_view(request):
    if request.is_ajax and request.method == "POST":
        booking_id = request.POST.get("bookingID")
        booking = get_object_or_404(BookingRequest, id=booking_id)
        # send email
        booking.status = "unbooked"
        booking.save()
        return JsonResponse({"result": "Success!"})

    raise Http404("Page Doesn't Exist!")


class BookmarkedView(LoginRequiredMixin, ListView):
    template_name = "users/my_bookmarks.html"
    context_object_name = "bookmarks"
    paginate_by = 10

    def get_queryset(self):
        return BookmarkedProperty.objects.filter(
            owner=self.request.user)


# class AddPropertyView(LoginRequiredMixin, CreateView):
#     template_name = "users/add_property.html"
#     form_class = PropertyForm


def add_property(request):
    if request.is_ajax and request.method == "POST":
        print('DATA: ', request.POST)
        print('FILES: ', request.FILES)

        property_form = PropertyForm(request.POST, prefix="form1")
        gallery_form = GalleryForm(request.POST, request.FILES)
        property_details_form = PropertyDetailsForm(
            request.POST, prefix="form2")

        print("errors: ", property_form.errors)

        if property_form.is_valid():

            print("did after!")

            property_obj = property_form.save(commit=False)
            property_obj.owner = Company.objects.get(manager=request.user.id)
            property_obj.save()

            gallery = gallery_form.save(commit=False)
            gallery.property_obj = property_obj
            gallery.save()

            property_details = property_details_form.save(commit=False)
            property_details.property_obj = property_obj
            property_details.save()

            return redirect(reverse("users:my-properties"))

    else:
        property_form = PropertyForm(prefix="form1")
        gallery_form = GalleryForm()
        property_details_form = PropertyDetailsForm(prefix="form2")

    return render(request, 'users/add_property.html', {
            'property_form': property_form,
            'gallery_form': gallery_form,
            'property_details_form': property_details_form
            })


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/my_account.html"


class UpdateAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/update_account.html"
