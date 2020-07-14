from django.urls import path

from .views import (add_hotel_view, hotel_details, hotel_booking_view,
                    # MyHotelBookingsView,
                    )

urlpatterns = [
    path('add-hotel/', add_hotel_view, name="add-hotel"),
    path('<int:pk>/', hotel_details, name="hotel-details"),
    path('room-booking/', hotel_booking_view, name="hotel-room-booking"),
    # path('hotel-bookings/', MyHotelBookingsView.as_view(), name="my-hotel-bookings"),
    # path('ajax/bookings/setup/', booking_setup_view, name="setup-bookings"),
    # path('ajax/bookings/delete/', booking_delete_view, name="delete-bookings"),
    # path('bookmarks/', BookmarkedView.as_view(), name="bookmarked"),
    # path('ajax/bookmarks/delete/', bookmark_delete_view, name="bookmark-delete"), 
]
