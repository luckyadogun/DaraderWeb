from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
            get_object_or_404, render,
            redirect, reverse)

from .forms import (
    PropertyForm,
    GalleryForm,
    PropertyDetailsForm,
    PropertyUpdateForm,
    DetailsUpdateForm
    )

from properties.models import (
    Property, Company,
    BookingRequest, Gallery,
    BookmarkedProperty,
    PropertyDetails)


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


@login_required
def add_property(request):
    if request.is_ajax and request.method == "POST":

        property_form = PropertyForm(request.POST, prefix="form1")
        gallery_form = GalleryForm(request.POST, request.FILES)
        property_details_form = PropertyDetailsForm(
            request.POST, prefix="form2")

        forms = all([
            property_form.is_valid(),
            gallery_form.is_valid(),
            property_details_form.is_valid()])

        if forms:
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


def update_property(request, pk=None):
    property_obj = get_object_or_404(Property, id=pk)
    gallery_obj = get_object_or_404(
        Gallery, property_obj=property_obj)
    prop_details = get_object_or_404(
        PropertyDetails, property_obj=property_obj)

    if request.is_ajax and request.method == "POST":

        property_form = PropertyUpdateForm(
            request.POST, instance=property_obj, prefix="form1")
        gallery_form = GalleryForm(
            request.POST, request.FILES, instance=gallery_obj)
        property_details_form = DetailsUpdateForm(
            request.POST, instance=prop_details, prefix="form2")

        forms = all([
                property_form.is_valid(),
                gallery_form.is_valid(),
                property_details_form.is_valid()])

        if forms:
            property_form.save()
            gallery_form.save()
            property_details_form.save()

            return redirect(reverse("users:my-properties"))
    else:
        property_form = PropertyUpdateForm(
            instance=property_obj, prefix="form1")
        gallery_form = GalleryForm(instance=gallery_obj)
        property_details_form = DetailsUpdateForm(
            instance=prop_details, prefix="form2")

    return render(request, 'users/update_property.html', {
            'property_form': property_form,
            'gallery_form': gallery_form,
            'property_details_form': property_details_form,
            'property': property_obj
            })


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

@login_required
def bookmark_delete_view(request):
    company = get_object_or_404(Company, manager=request.user)

    if request.is_ajax and request.method == "POST":
        bookmark_id = request.POST.get("bookmarkID")
        bookmark = get_object_or_404(BookmarkedProperty, id=bookmark_id)

        if bookmark.property_obj.owner == company:
            bookmark.delete()
            return JsonResponse({"result": "Success!"})
        return JsonResponse({"result": "Unauthorized Access!"})

    raise Http404("Page Doesn't Exist!")


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/my_account.html"


class UpdateAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/update_account.html"
