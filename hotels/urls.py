from django.urls import path

from .views import (add_hotel_view, hotel_details, hotel_booking_view, 
                    MyHotelView, update_hotel, hotel_delete_view, AllHotelView
                    )

urlpatterns = [
    path('add-hotel/', add_hotel_view, name="add-hotel"),
    path('<str:name>', hotel_details, name="hotel-details"),
    path('room-booking/', hotel_booking_view, name="hotel-room-booking"),
    path('<str:name>/update/', update_hotel, name="update-hotel"),
    path('ajax/hotel/delete/', hotel_delete_view, name="delete-hotel"),
    path('my-hotels/', MyHotelView.as_view(), name="my-hotels"),
    path('all-hotels/', AllHotelView.as_view(), name="all-hotels")
    # path('hotel-bookings/', MyHotelBookingsView.as_view(), name="my-hotel-bookings"),
    # path('ajax/bookings/setup/', booking_setup_view, name="setup-bookings"),
    # path('ajax/bookings/delete/', booking_delete_view, name="delete-bookings"),
    # path('bookmarks/', BookmarkedView.as_view(), name="bookmarked"),
    # path('ajax/bookmarks/delete/', bookmark_delete_view, name="bookmark-delete"), 
]
