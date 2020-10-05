from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout, authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from .serializers import AuthSerializer, HotelSerializer, PropertySerializer, UserSerializer, IdSerializer, UpdateUserSerializer, BookRoomSerializer
from users.models import User
from hotels.models import Hotel, BookmarkedHotel, Room
from properties.models import Property, BookmarkedProperty
from properties.helpers import email_activate_acct, get_currently_featured
from hotels.helpers import hotel_email_booking_request, user_hotel_email_booking_request
# Create your views here.

class RegisterView(APIView):
    serializer_class = AuthSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=email).exists():
                return Response({
                    "code": 110,
                    "message": "user already exist",
                    "resolve": "Proceed to login"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                user = User.objects.create(email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                # User.is_active is defaultly set to false and need email confirmation to activate
                email_activate_acct(request, user)
                return Response({
                    "code": 201,
                    "message": "Successful",
                    "resolve": "User Successfully created"
                    }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = AuthSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'code': 200,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': request.user.email
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "code": 110,
                        "message": "inactive user",
                        "resolve": "proceed to activate your account"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                    return Response({
                        "code": 120,
                        "message": "invalid crendetials",
                        "resolve": "There's no account matching this email and password"
                    }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def patch(self, request):
        user = request.user
        email = request.data.get('email')
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        phoneNumber = request.data.get('phoneNumber')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if User.objects.exclude(id=user.id).filter(email=email).exists():
                return Response({
                    'code': 110,
                    'message': 'user with that mail already exist',
                    'resolve': 'Enter a valid email'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                user.mobile_phone = phoneNumber
                user.save()
                return Response({
                    'code': 200,
                    'message': 'Successful',
                    'resolve': 'Account updated successfully'
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyView(ListAPIView):
    queryset = Property.objects.all()
    permission_classes = []
    serializer_class = PropertySerializer
    filter_backends = (SearchFilter, OrderingFilter)
    # 'state__name', 'country__name', 'owner__name', 'market_status', 'price', 'description'
    search_fields = ('title', 'address', 'lga__name', 'property_type', 'property_category')

class HotelView(ListAPIView):
    queryset = Hotel.objects.all()
    permission_classes = []
    serializer_class = HotelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'address', 'hotel_type', "room__room_name")

class FeaturedPropertyView(ListAPIView):
    queryset = get_currently_featured()
    permission_classes = []
    serializer_class = PropertySerializer

class BookmarkPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # bookmarked_properties = BookmarkedProperty.objects.filter(owner=request.user)
        bookmarked_properties = Property.objects.filter(bookmarked__owner=request.user)
        serializer = PropertySerializer(bookmarked_properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.data.get('id')
        serializer = IdSerializer(data = request.data)
        if serializer.is_valid():
            try:
                property_instance = Property.objects.get(id=id)
                try:
                    BookmarkedProperty.objects.get(owner=request.user, property_obj=property_instance)
                    return Response({
                        "code": 120,
                        "message": "property bookmarked already",
                        "resolve": "already in your hotels bookmarked"
                    }, status=status.HTTP_208_ALREADY_REPORTED)
                except BookmarkedProperty.DoesNotExist:
                    BookmarkedProperty.objects.create(owner=request.user, property_obj=property_instance)
                    return Response({
                        "code": 120,
                        "message": "property bookmarked successfully"
                    }, status=status.HTTP_201_CREATED)
            except Property.DoesNotExist:
                return Response({
                    "code": 120,
                    "message": "property does not exist",
                    "resolve": "Incorrect property id"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkHotelView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # bookmarked_hotels = BookmarkedHotel.objects.filter(owner=request.user)
        bookmarked_hotels = Hotel.objects.filter(bookmarkedHotel__owner=request.user)
        serializer = HotelSerializer(bookmarked_hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.data.get('id')
        room_id = request.data.get('room_id')
        serializer = BookRoomSerializer(data = request.data)
        if serializer.is_valid():
            try:
                hotel_instance = Hotel.objects.get(id=id)
                try:
                    BookmarkedHotel.objects.get(owner=request.user, hotel=hotel_instance)
                    return Response({
                        "code": 120,
                        "message": "hotel bookmarked already",
                        "resolve": "already in your hotel bookmarked"
                    }, status=status.HTTP_208_ALREADY_REPORTED)
                except BookmarkedHotel.DoesNotExist:
                    try:   
                        room_instance = Room.objects.get(hotel=hotel_instance, pk=room_id)
                        hotel_email = hotel_instance.creator.email
                        hotel_name = hotel_instance.name
                        room_name = room_instance.room_name
                        user_name = request.user.username
                        user_email = request.user.email
                        BookmarkedHotel.objects.create(owner=request.user, hotel=hotel_instance)     
                        hotel_email_booking_request(hotel_email, hotel_name, user_name, room_name, user_email)        
                        user_hotel_email_booking_request(user_email, user_name, room_name, hotel_name)
                        return Response({
                            "code": 120,
                            "message": "room booking request sent successfully"
                        }, status=status.HTTP_201_CREATED)
                    except Room.DoesNotExist:
                        return Response({
                        "code": 121,
                        "message": "room does not exist",
                        "resolve": "Incorrect room id"
                    }, status=status.HTTP_404_NOT_FOUND)
            except Hotel.DoesNotExist:
                return Response({
                    "code": 120,
                    "message": "hotel does not exist",
                    "resolve": "Incorrect hotel id"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)