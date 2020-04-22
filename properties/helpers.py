import random

from django.shortcuts import reverse
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from project.settings import send_email, INTERNAL_EMAIL

from users.models import User

from .models import Company, Property
from .utils import account_activation_token


def email_activate_acct(request, user_pk):
    user = User.objects.get(id=user_pk)
    URI = request.build_absolute_uri(reverse("properties:activate"))
    subject = 'Activate your account'
    message = render_to_string('properties/email/activate_account.html', {
        'user': f"{user}",
        'domain': URI,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_email(recipient=user.email, subject=subject, html_content=message)


def email_booking_request(request, user_pk):
    user = User.objects.get(id=user_pk)
    URI = request.build_absolute_uri(reverse("users:my-bookings"))
    subject = 'You have a booking request'
    message = render_to_string('properties/email/new_booking.html', {
        'user': f"{user}",
        'domain': URI
    })
    send_email(recipient=user.email, subject=subject, html_content=message)


def email_contact_us(data):
    subject = 'You have a booking request'
    message = render_to_string('properties/email/contact_us.html', {
        "contact_name": data["name"],
        "contact_email": data["email"],
        "contact_message": data["message"],
    })
    send_email(recipient=INTERNAL_EMAIL, subject=subject, html_content=message)


def get_currently_featured():
    """
    Here we use randomly select a featured
    company and list their property on the
    `HomePageView`

    """
    featured_companies = Company.objects.filter(
        is_approved=True, is_featured=True)
    total_featured_companies = featured_companies.count()
    try:
        currently_featured = featured_companies[
            random.randrange(0, total_featured_companies)]
        return currently_featured.property.all()[:5]
    except ValueError:
        return Property.objects.all()[:5]