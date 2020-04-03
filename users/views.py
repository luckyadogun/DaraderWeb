from django.urls import reverse
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.deprecation import MiddlewareMixin

from properties.models import Property, Company


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["recent_properties"] = Property.objects.order_by("created")[:3]

        return context


class MyPropertyView(ListView):
    template_name = "users/my_properties.html"
    context_object_name = "properties"
    paginate_by = 5

    def get_queryset(self):
        company = Company.objects.get(manager=self.request.user)
        return Property.objects.filter(owner=company)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PropertyDeleteView(DeleteView):
    model = Property
    template_name = "users/property_delete.html"
    success_url = reverse_lazy("users:my-properties")

    def get_queryset(self):
        company = Company.objects.get(manager=self.request.user)
        return self.model.objects.filter(owner=company)


def property_delete_view(request, pk=None):
    if request.is_ajax and request.method == "POST":
        property_id = request.POST.get("propertyID")
        print(property_id)
        # check if property_id == pk and owner
        # use get_object_or_404(id=property_id)
        # delete object
        return JsonResponse({"result": "Success!"})


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