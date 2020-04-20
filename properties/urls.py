from django.urls import path

from .views import (
    HomePageView, SearchResultView,
    login_view, password_recovery,
    logout_view, signup_view,
    bookmark_item_view, property_details
    )

urlpatterns = [
    path('ajax/signup', signup_view, name="signup"),
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
        property_details, name="property-details"),
    path(
        'ajax/bookmark', bookmark_item_view, name="bookmark-property"),
    path('forgot-password', password_recovery, name="forgot-password"),
]