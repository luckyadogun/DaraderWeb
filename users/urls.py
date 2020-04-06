from django.urls import path

from .views import (
    DashboardView, MyPropertyView,
    MyBookingsView, AddPropertyView,
    MyAccountView, UpdateAccountView,
    BookmarkedView, property_delete_view,
    booking_delete_view, booking_setup_view)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('properties', MyPropertyView.as_view(), name="my-properties"),
    path('ajax/properties/delete', property_delete_view, name="delete-property"),
    path('bookings', MyBookingsView.as_view(), name="my-bookings"),
    path('ajax/bookings/setup', booking_setup_view, name="setup-bookings"),
    path('ajax/bookings/delete', booking_delete_view, name="delete-bookings"),
    path('favourites', BookmarkedView.as_view(), name="bookmarked"),
    path('add-property', AddPropertyView.as_view(), name="add-property"),
    path('account', MyAccountView.as_view(), name="account"),
    path('account/update', UpdateAccountView.as_view(), name="update-account"),
]
