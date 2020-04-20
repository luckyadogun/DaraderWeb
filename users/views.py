from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from django.contrib import messages
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
    DetailsUpdateForm,
    GalleryUpdateForm,
    AccountUpdateForm,
    CompanyForm, CompanyUpdateForm
    )

from .decorators import manager_required

from properties.models import (
    Property, Company,
    BookingRequest, Gallery,
    BookmarkedProperty,
    PropertyDetails)


@method_decorator([login_required], name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_properties"] = Property.objects.order_by("created")[:3]

        return context


@method_decorator([login_required], name='dispatch')
class MyPropertyView(LoginRequiredMixin, ListView):
    template_name = "users/my_properties.html"
    context_object_name = "properties"
    paginate_by = 5

    def get_queryset(self):
        company = Company.objects.get(manager=self.request.user)
        return Property.objects.filter(owner=company)


@login_required
@manager_required
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
@manager_required
def add_property(request):
    context = {}

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

            uploaded_images = request.FILES.getlist('image') or request.FILES.get('image')

            for img in uploaded_images:
                gallery = Gallery(
                    property_obj=property_obj,
                    image=img)
                gallery.save()

            property_details = property_details_form.save(commit=False)
            property_details.property_obj = property_obj
            property_details.save()

            return redirect(reverse("users:my-properties"))

    else:
        property_form = PropertyForm(prefix="form1")
        gallery_form = GalleryForm()
        property_details_form = PropertyDetailsForm(prefix="form2")

    context["property_form"] = property_form
    context["gallery_form"] = gallery_form
    context["property_details_form"] = property_details_form

    return render(request, 'users/add_property.html', context)


@login_required
@manager_required
def update_property(request, pk=None):
    context = {}

    property_obj = get_object_or_404(Property, id=pk)
    prop_details = get_object_or_404(
        PropertyDetails, property_obj=property_obj)

    if request.is_ajax and request.method == "POST":

        property_form = PropertyUpdateForm(
            request.POST, instance=property_obj, prefix="form1")
        gallery_form = GalleryUpdateForm(request.POST, request.FILES)
        property_details_form = DetailsUpdateForm(
            request.POST, instance=prop_details, prefix="form2")

        forms = all([
                property_form.is_valid(),
                gallery_form.is_valid(),
                property_details_form.is_valid()])

        if forms:
            property_obj = property_form.save()
            property_details_form.save()

            uploaded_images = request.FILES.getlist('image')

            for img in uploaded_images:
                gallery = Gallery(
                    property_obj=property_obj,
                    image=img)
                gallery.save()

            return redirect(reverse("users:my-properties"))
    else:
        property_form = PropertyUpdateForm(
            instance=property_obj, prefix="form1")
        gallery_form = GalleryUpdateForm()
        property_details_form = DetailsUpdateForm(
            instance=prop_details, prefix="form2")

    context["property_form"] = property_form
    context["gallery_form"] = gallery_form
    context["property_details_form"] = property_details_form
    context["property"] = property_obj

    return render(request, 'users/update_property.html', context)


@method_decorator([login_required], name='dispatch')
class MyBookingsView(LoginRequiredMixin, ListView):
    template_name = "users/my_bookings.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):
        return BookingRequest.objects.filter(
            company__manager=self.request.user,
            status="booked")


@login_required
@manager_required
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
@manager_required
def booking_setup_view(request):
    if request.is_ajax and request.method == "POST":
        booking_id = request.POST.get("bookingID")
        booking = get_object_or_404(BookingRequest, id=booking_id)
        # send email
        booking.status = "unbooked"
        booking.save()
        return JsonResponse({"result": "Success!"})

    raise Http404("Page Doesn't Exist!")


@method_decorator([login_required], name='dispatch')
class BookmarkedView(LoginRequiredMixin, ListView):
    template_name = "users/my_bookmarks.html"
    context_object_name = "bookmarks"
    paginate_by = 10

    def get_queryset(self):
        return BookmarkedProperty.objects.filter(
            owner=self.request.user)


@login_required
@manager_required
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


@method_decorator([login_required], name='dispatch')
class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/my_account.html"


@login_required
@manager_required
def account_update_view(request):
    context = {}

    if request.method == "POST":
        account_form = AccountUpdateForm(request.POST, instance=request.user)

        if account_form.is_valid():
            user = account_form.save(commit=False)
            user.set_password(account_form.cleaned_data["new_password2"])
            user.save()

            return redirect(reverse("properties:home"))
        else:
            messages.error(request, account_form.errors)
    else:
        account_form = AccountUpdateForm(instance=request.user)

    context["account_form"] = account_form
    return render(request, 'users/update_account.html', context)


@login_required
@manager_required
def add_company_view(request):
    context = {}

    if request.method == "POST":
        company_form = CompanyForm(
            request.POST, request.FILES)

        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.manager = request.user
            logo = request.FILES.get("logo")

            if logo:
                company.logo = logo
            company.save()

            return redirect(reverse("users:dashboard"))
        else:
            messages.error(request, company_form.errors)

    else:
        company_form = CompanyForm()

    context["company_form"] = company_form
    return render(request, 'users/add_company.html', context)


@login_required
@manager_required
def update_company_view(request):
    context = {}

    company_obj = Company.objects.get(manager=request.user)

    if request.method == "POST":
        company_form = CompanyUpdateForm(
            request.POST, request.FILES,
            instance=company_obj)

        if company_form.is_valid():
            company = company_form.save(commit=False)
            logo = request.FILES.get("logo")

            if logo:
                company.logo = logo
            company.save()

            return redirect(reverse("users:update-company"))
        else:
            messages.error(request, company_form.errors)

    else:
        company_form = CompanyUpdateForm(instance=company_obj)

    context["company_form"] = company_form
    context["company"] = company_obj
    return render(request, 'users/update_company.html', context)
