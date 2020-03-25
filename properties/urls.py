from django.urls import path

from .views import (
    HomePageView, 
    SearchResultView,
    PropertyDetailView)


urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('search/', SearchResultView.as_view(), name="search"),
    path('property/<int:pk>/<slug>/', PropertyDetailView.as_view(), name="property-details"),
]
