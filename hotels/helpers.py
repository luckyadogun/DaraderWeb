from django.template.loader import render_to_string
from project.settings import send_email

def hotel_email_booking_request(hotel_email, hotel_name, user_name, room_name, user_email):
    # URI = request.build_absolute_uri(reverse("users:my-bookings"))
    subject = 'You have a room booking request'
    message = render_to_string('hotels/email/hotel_email_booking.html', {
        'hotel_name': hotel_name,
        'user_name': user_name,
        'room_name':room_name,
        'user_email':user_email
    })
    send_email(recipient=hotel_email, subject=subject, html_content=message)

def user_hotel_email_booking_request(user_email, user_name, room_name, hotel_name):
    # URI = request.build_absolute_uri(reverse("users:my-bookings"))
    subject = 'Room booking request'
    message = render_to_string('hotels/email/user_hotel_email_booking.html', {
        'user_name': user_name,
        'room_name': room_name,
        'hotel_name': hotel_name
    })
    send_email(recipient=user_email, subject=subject, html_content=message)