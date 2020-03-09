from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

from .models import Property


class HomePageView(TemplateView):

    template_name = "properties/home.html"

    def get_context_data(self, **kwargs):
        # TODO
        # - add dummy properties
        # - add properties to context
        # - edit html code with for-loop
        
        context = super().get_context_data(**kwargs)
        context['for_sale'] = Property.forsale.order_by('created')[:5]
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
        property_status = self.request.POST.get("property-status", "")
        bedroom_size = self.request.POST.get("bedrooms", "")
        bathrooms = self.request.POST.get("bathrooms", "")
        budget = self.request.POST.get("budget", "")

        return render(request, self.template_name, {})