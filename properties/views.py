from itertools import chain

from django.urls import reverse
from django.core import serializers
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

from .models import Property, PropertyDetails
from .utils import get_currently_featured


class HomePageView(TemplateView):

    template_name = "properties/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['for_sale'] = Property.forsale.order_by('created')[:3]
        context['for_rent'] = Property.forrent.order_by('created')[:3]
        context['for_lease'] = Property.forlease.order_by('created')[:3]
        context['recent_properties'] = Property.objects.order_by('created')[:7]
        context['featured'] = get_currently_featured()

        return context

    def post(self, request, *args, **kwargs):
        # TODO:
        # - add fallback
        # - split budget
        # - call models and filter
        # - return a response with data
        # - add unit test

        search_title = self.request.POST.get("location", "")
        property_type = self.request.POST.get("property-type", "")
        property_category = self.request.POST.get("property-category", "")
        bedrooms = self.request.POST.get("bedrooms", 1)
        bathrooms = self.request.POST.get("bathrooms", 1)
        budget = self.request.POST.get("budget").split('-')

        q1 = PropertyDetails.objects.filter(
            property_obj__title__icontains=search_title)
        q2 = PropertyDetails.objects.filter(
            property_obj__property_type=property_type)
        q3 = PropertyDetails.objects.filter(
            property_obj__property_category=property_category)
        q4 = PropertyDetails.objects.filter(bedrooms=int(bedrooms))
        q5 = PropertyDetails.objects.filter(bathrooms=int(bathrooms))
        q6 = PropertyDetails.objects.filter(
            property_obj__price__range=(
                int(budget[0]), int(budget[1])))

        query = list(set(chain(q1, q2, q3, q4, q5)))
        data = serializers.serialize("json", query)
        self.request.session['query'] = data

        return HttpResponseRedirect('/search/')


class SearchResultView(TemplateView):

    template_name = "properties/serp.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'query' in self.request.session:
            print(self.request.session['query'])

        return context
