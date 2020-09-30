from django.test import TestCase, Client
from django.http import HttpRequest
import json
from rest_framework import status
from django.urls import reverse
from users.models import User
from hotels.models import Hotel
from properties.models import Property

# Create your tests here.
client = Client()

class UserInstance(TestCase):
    def setUp(self):
        self.exist_user = {
            'email':'fakeuser@test.com',
            'password':'fakepassword'
        }
        self.valid_payload = {
            'email':'fakeuser1@test.com',
            'password':'fakepassword'
        }
        self.invalid_payload = {
            'email':'',
            'password':'password'
        }
        self.wrong_payload = {
            'email':'wronguser@test.com',
            'password':'password'
        }

class LoginTest(UserInstance):
    """ Test module for logging a user in"""
    def test_login_valid_with_unregistered_user(self):
        response = client.post(reverse('api:login'), data=json.dumps(self.wrong_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_valid_with_active_user(self):
        User.objects.create_user(**self.valid_payload)
        response = client.post(reverse('api:login'), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Having issue with setting user.is_active=False in test mode
    # def test_login_valid_with_inactive_user(self):
    #     user = User.objects.create_user(**self.valid_payload)
    #     user.is_active = False
    #     user.save()
    #     response = client.post(reverse('api:login'), data=json.dumps(self.valid_payload), content_type='application/json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid(self):
        response = client.post(reverse('api:login'), data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SignUpTest(UserInstance):
    """ Test module for signing a user up"""
    def test_user_exist(self):
        User.objects.create_user(**self.exist_user)
        response = client.post(reverse('api:register'), data=json.dumps(self.exist_user), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_signup_valid(self):
        response = client.post(reverse('api:register'), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_signup_invalid(self):
        response = client.post(reverse('api:register'), data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetHotelTest(UserInstance):
    """ Test module for getting hotels list """
    def test_get_hotels_without_auth(self):
        response = client.get(reverse('api:hotels'))
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # def test_get_hotels_with_auth(self):
    #     User.objects.create_user(**self.valid_payload)
    #     login_response = client.post(reverse('api:login'), data=json.dumps(self.valid_payload), content_type='application/json')
    #     login_response_dict = login_response.json()
    #     access_token = login_response_dict['access']
    #     response = client.get(reverse('api:hotels'), HTTP_AUTHORIZATION=f'Bearer {access_token}')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetPropertyTest(UserInstance):
    """ Test module for getting hotels list """
    def test_get_properties_without_auth(self):
        response = client.get(reverse('api:properties'))
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # def test_get_properties_with_auth(self):
    #     User.objects.create_user(**self.valid_payload)
    #     login_response = client.post(reverse('api:login'), data=json.dumps(self.valid_payload), content_type='application/json')
    #     login_response_dict = login_response.json()
    #     access_token = login_response_dict['access']
    #     response = client.get(reverse('api:properties'), HTTP_AUTHORIZATION=f'Bearer {access_token}')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookmarkHotelTest(UserInstance):
    """ Test module for booking hotel """
    def test_get_bookmark_hotel_without_auth(self):
        response = client.get(reverse('api:bookmark-hotel'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_post_bookmark_hotel_without_auth(self):
        response = client.post(reverse('api:bookmark-hotel'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_get_bookmark_hotel_with_auth(self):
        User.objects.create_user(**self.valid_payload)
        login_response = client.post(reverse('api:login'), data=json.dumps(self.valid_payload), content_type='application/json')
        login_response_dict = login_response.json()
        access_token = login_response_dict['access']
        response = client.get(reverse('api:bookmark-hotel'), HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_post_bookmark_hotel_with_auth_and_empty_body(self):
        User.objects.create_user(**self.valid_payload)
        login_response = client.post(reverse('api:login'), data=json.dumps(self.valid_payload), content_type='application/json')
        login_response_dict = login_response.json()
        access_token = login_response_dict['access']
        response = client.post(reverse('api:bookmark-hotel'), HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    