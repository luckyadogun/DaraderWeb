from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "properties/home.html"

    # def get(self, *args, **kwargs):
    #     return HttpResponse("Hello World!")
