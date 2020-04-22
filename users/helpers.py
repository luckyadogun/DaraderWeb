from django.template.loader import render_to_string

from project.settings import send_email


def email_booking_confirmed(booking):
    client = booking.client
    subject = 'You booking has been approved!'
    message = render_to_string('properties/email/new_booking.html', {
        'client': f"{client}",
        'property': booking.property_obj,
        'owner': booking.property_details.property_obj.owner
    })
    send_email(recipient=client.email, subject=subject, html_content=message)