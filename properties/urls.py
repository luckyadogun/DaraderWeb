from django.urls import path

from .views import (
    HomePageView, SearchResultView,
    PropertyDetailView, login_view,
    logout_view
    )

urlpatterns = [
    path('ajax/login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('', HomePageView.as_view(), name="home"),
    path(
        'search', SearchResultView.as_view(), 
        {"queryset": "search"}, name="search"),
    path(
        'rent', SearchResultView.as_view(),
        {"queryset": "rent"}, name="rent"),
    path(
        'sale', SearchResultView.as_view(),
        {"queryset": "sale"}, name="sale"),
    path(
        'lease', SearchResultView.as_view(),
        {"queryset": "lease"}, name="lease"),
    path(
        'all', SearchResultView.as_view(),
        {"queryset": "all"}, name="all"),
    path(
        'flats', SearchResultView.as_view(),
        {"queryset": "flat"}, name="flats"),
    path(
        'lands/', SearchResultView.as_view(),
        {"queryset": "land"}, name="lands"), 
    path(
        'houses', SearchResultView.as_view(),
        {"queryset": "house"}, name="houses"),
    path(
        'commercial-spaces', SearchResultView.as_view(),
        {"queryset": "commercial"}, name="commercial_spaces"),
    path(
        'event-centres', SearchResultView.as_view(),
        {"queryset": "event centre"}, name="event_centres"),
    path(
        'property/<int:pk>/<slug>/',
        PropertyDetailView.as_view(), name="property-details"),
]
