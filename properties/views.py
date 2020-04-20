from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import (
    render_to_response,
    redirect, render,
    get_object_or_404)
from django.contrib.auth import login, logout, authenticate

from users.models import User
from users.forms import UserCreationForm

from .models import (
    Property, PropertyDetails,
    BookingRequest, BookmarkedProperty as Bookmarked)
from .forms import BookingRequestForm as BRForm
from .utils import get_currently_featured


def signup_view(request):
    if request.is_ajax and request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            # send email and redirect to acct activation
            # redirect from activation to dashboard
            # return redirect(reverse("users:dashboard"))
            return JsonResponse({"result": "Success"})
        else:
            return JsonResponse({"result": "Failed"})
    raise Http404("Page Doesn't Exist!")


def login_view(request):
    if request.is_ajax and request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            username=username,
            password=password
            )
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({"result": "Success!"})
        else:
            return JsonResponse({"result": "Failed!"})

    raise Http404("Page Doesn't Exist!")


def logout_view(request):
    logout(request)
    return redirect(reverse("properties:home"))


class HomePageView(TemplateView):

    template_name = "properties/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["for_sale"] = Property.forsale.order_by("created")[:3]
        context["for_rent"] = Property.forrent.order_by("created")[:3]
        context["for_lease"] = Property.forlease.order_by("created")[:3]
        context["recent_properties"] = Property.objects.order_by("created")[:7]
        context["featured"] = get_currently_featured()

        return context

    def post(self, request, *args, **kwargs):
        search_title = self.request.POST.get("location", "")
        property_type = self.request.POST.get("property-type", "")
        property_category = self.request.POST.get("property-category", "")
        bedrooms = self.request.POST.get("bedrooms", 1)
        bathrooms = self.request.POST.get("bathrooms", 1)
        budget = self.request.POST.get("budget", "200000 - 300000").split("-")

        query = PropertyDetails.objects.filter(
            Q(property_obj__title__icontains=search_title) |
            Q(property_obj__property_type=property_type) |
            Q(property_obj__property_category=property_category) |
            Q(bedrooms=int(bedrooms)) | Q(bathrooms=int(bathrooms)) |
            Q(property_obj__price__range=(int(budget[0]), int(budget[1])))
            )

        self.request.session["query"] = list(set([qs.pk for qs in query]))
        return HttpResponseRedirect(reverse("properties:search"))


class SearchResultView(ListView):

    template_name = "properties/serp.html"
    context_object_name = "properties"
    paginate_by = 5

    def get_queryset(self):

        search_title = self.request.GET.get("location", "")
        property_type = self.request.GET.get("property-type", "")
        property_category = self.request.GET.get("property-category", "")
        bedrooms = self.request.GET.get("bedrooms", 1)
        bathrooms = self.request.GET.get("bathrooms", 1)
        budget = self.request.GET.get("budget", "200000 - 300000").split("-")
        basketball = self.request.GET.get("basketball")
        swimming_pool = self.request.GET.get("swimming-pool")
        gym = self.request.GET.get("gym")
        wheelchair = self.request.GET.get("wheelchair")

        submit_action = self.request.GET.get("submit")

        new_query = PropertyDetails.objects.filter(
            Q(property_obj__title__icontains=search_title) |
            Q(property_obj__property_type=property_type) |
            Q(property_obj__property_category=property_category) |
            Q(bedrooms=int(bedrooms)) | Q(bathrooms=int(bathrooms)) |
            Q(property_obj__price__range=(int(budget[0]), int(budget[1]))) |
            Q(has_basketball_court=bool(basketball)) |
            Q(has_swimming_pool=bool(swimming_pool)) | Q(has_gym=bool(gym)) |
            Q(is_wheelchair_friendly=bool(wheelchair))
            )

        category_param = ["rent", "sale", "lease", ]

        type_param = [
            "flat", "land",
            "house", "commercial",
            "event centre", ]

        if self.kwargs["queryset"] == "search":
            if submit_action:
                return new_query
            else:
                try:
                    return [PropertyDetails.objects.get(pk=qs) for qs in self.request.session["query"]]
                except KeyError:
                    return ""

        if self.kwargs["queryset"] in category_param:
            if submit_action:
                return new_query
            else:
                return PropertyDetails.objects.filter(
                    property_obj__property_category=self.kwargs["queryset"])

        if self.kwargs["queryset"] in type_param:
            if submit_action:
                return new_query
            else:
                return PropertyDetails.objects.filter(
                    property_obj__property_type=self.kwargs["queryset"])

        if self.kwargs["queryset"] == "all":
            if submit_action:
                return new_query
            else:
                return PropertyDetails.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = self.request.META["QUERY_STRING"]
        context["recent_properties"] = Property.objects.order_by("created")[:5]
        context["total_flats"] = Property.objects.filter(
                                    property_type="flat").count()
        context["total_houses"] = Property.objects.filter(
                                    property_type="house").count()
        context["total_lands"] = Property.objects.filter(
                                    property_type="land").count()
        context["total_commercials"] = Property.objects.filter(
                                    property_type="commercial").count()
        context["total_event_centres"] = Property.objects.filter(
                                    property_type="event centre").count()
        return context


def property_details(request, pk, slug):
    context = {}

    obj = PropertyDetails.objects.get(
        property_obj__id=pk,
        property_obj__slug=slug)

    if request.method == "POST":
        bookingform = BRForm(request.POST)

        if bookingform.is_valid():
            booking_obj = bookingform.save(commit=False)
            booking_obj.company = obj.property_obj.owner
            booking_obj.property_details = obj
            booking_obj.client = request.user
            booking_obj.status = "booked"
            booking_obj.save()

            # send email
            messages.success(request, "Successfully Booked!")
        else:
            messages.error(request, bookingform.errors)

    else:
        bookingform = BRForm()

    context["object"] = obj
    context["recent_properties"] = Property.objects.order_by("created")[:3]
    context["featured"] = get_currently_featured()
    context["images"] = [x.image.url for x in obj.property_obj.gallery.all()]
    context["similar"] = PropertyDetails.objects.filter(
        Q(property_obj__title__icontains=obj.property_obj.title) |
        Q(property_obj__property_type=obj.property_obj.property_type) |
        Q(property_obj__area=obj.property_obj.area) |
        Q(property_obj__owner=obj.property_obj.owner)
    )
    context["bookingform"] = bookingform

    return render(request, 'properties/single-property.html', context)


def bookmark_item_view(request):
    if request.is_ajax and request.method == "POST":
        property_id = request.POST.get('propertyID')

        if request.user.is_authenticated:
            property_obj = get_object_or_404(Property, id=property_id)

            try:
                Bookmarked.objects.get(
                    owner=request.user,
                    property_obj=property_obj)
                return JsonResponse({"result": "Already Bookmarked!"})
            except Bookmarked.DoesNotExist:
                Bookmarked.objects.create(
                    owner=request.user, property_obj=property_obj)
                return JsonResponse({"result": "Success!"})

        return JsonResponse({"result": "Unauthorized"})
    else:
        raise Http404("Page Doesn't Exist!")


def password_recovery(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            new_password = get_random_string()
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # send email
            messages.success(request, f"New password sent to: {email}")
        else:
            messages.error(request, f"User with that email doesn't exist!")
    return render(request, 'properties/auth/password_recovery.html', {})


def handler404(request, exception, template_name="properties/404.html"):
    response = render_to_response(
        template_name)
    response.status = 404
    return response
