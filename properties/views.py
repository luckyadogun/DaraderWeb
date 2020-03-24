from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect

from .models import Property, PropertyDetails
from .utils import get_currently_featured


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
        return HttpResponseRedirect(reverse("search"))


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
        if len(new_query) != 0:
            return new_query
        else:
            return [PropertyDetails.objects.get(pk=qs) for qs in self.request.session["query"]]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = self.request.META["QUERY_STRING"]
        context["recent_properties"] = Property.objects.order_by("created")[:5]
        context["total_properties"] = Property.objects.count()
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


class PropertyDetailView(DetailView):
    context_object_name = "property"
    template_name = "properties/single-property.html"
    model = PropertyDetails

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_properties"] = Property.objects.order_by("created")[:3]
        context["featured"] = get_currently_featured()
        
        return context
