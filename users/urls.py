from django.urls import path

from .views import (
    DashboardView, MyPropertyView,
    MyBookingsView, AddPropertyView,
    MyAccountView, UpdateAccountView,
    BookmarkedView
    )

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path(
        'properties/active',
        MyPropertyView.as_view(),
        {"queryset": "active"}, name="active-properties"),
    path(
        'properties/inactive',
        MyPropertyView.as_view(),
        {"queryset": "inactive"}, name="inactive-properties"),
    path('bookings', MyBookingsView.as_view(), name="my-bookings"),
    path('favourites', BookmarkedView.as_view(), name="bookmarked"),
    path('add-property', AddPropertyView.as_view(), name="add-property"),
    path('account', MyAccountView.as_view(), name="account"),
    path('account/update', UpdateAccountView.as_view(), name="update-account"),
]
