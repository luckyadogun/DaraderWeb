from django.urls import path

from .views import (
    DashboardView, MyPropertyView,
    MyBookingsView, add_property,
    MyAccountView, account_update_view,
    BookmarkedView, property_delete_view,
    booking_delete_view, booking_setup_view,
    update_property,  bookmark_delete_view,
    add_company_view, update_company_view)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('properties', MyPropertyView.as_view(), name="my-properties"),
    path('add-property', add_property, name="add-property"),
    path(
        'ajax/properties/delete',
        property_delete_view, 
        name="delete-property"),
    path('property/<int:pk>/update', update_property, name="update-property"),
    path('bookings', MyBookingsView.as_view(), name="my-bookings"),
    path('ajax/bookings/setup', booking_setup_view, name="setup-bookings"),
    path('ajax/bookings/delete', booking_delete_view, name="delete-bookings"),
    path('bookmarks', BookmarkedView.as_view(), name="bookmarked"),
    path('ajax/bookmarks/delete', bookmark_delete_view, name="bookmark-delete"),
    path('account', MyAccountView.as_view(), name="account"),
    path('account/update', account_update_view, name="update-account"),
    path('company/add', add_company_view, name="add-company"),
    path('company/update', update_company_view, name="update-company"),
]
