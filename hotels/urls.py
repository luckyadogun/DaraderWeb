from django.urls import path

from .views import add_hotel_view

urlpatterns = [
    path('add-hotel/', add_hotel_view, name="add-hotel"), 
]
