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

from .serializers import AuthSerializer, HotelSerializer, PropertySerializer, UserSerializer, IdSerializer, BookmarkedPropertySerializer, BookmarkedHotelSerializer
from users.models import User
from hotels.models import Hotel, BookmarkedHotel
from properties.models import Property, BookmarkedProperty
from properties.helpers import email_activate_acct
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
                    "code": 150,
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
                    "code": 200,
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
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': request.user.email
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "code": 0,
                        "message": "inactive user",
                        "resolve": "proceed to activate your account"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                    return Response({
                        "code": 120,
                        "message": "invalid crendetials",
                        "resolve": "The email or password is not correct."
                    }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        # auth_header = request.META['HTTP_AUTHORIZATION']
        # token = auth_header.split(' ')[1]
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyView(ListAPIView):
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    filter_backends = (SearchFilter, OrderingFilter)
    # 'state__name', 'country__name', 'owner__name', 'market_status', 'price', 'description'
    search_fields = ('title', 'address', 'lga__name', 'property_type', 'property_category')

class HotelView(ListAPIView):
    queryset = Hotel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'address', 'hotel_type', "room__room_name")

class BookmarkPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkedPropertySerializer
    
    def get(self, request):
        bookmarked_properties = BookmarkedProperty.objects.filter(owner=request.user)
        serializer = self.serializer_class(bookmarked_properties, many=True)
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
    serializer_class = BookmarkedHotelSerializer
    
    def get(self, request):
        bookmarked_hotels = BookmarkedHotel.objects.filter(owner=request.user)
        serializer = self.serializer_class(bookmarked_hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.data.get('id')
        serializer = IdSerializer(data = request.data)
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
                    BookmarkedHotel.objects.create(owner=request.user, hotel=hotel_instance)
                    return Response({
                        "code": 120,
                        "message": "hotel bookmarked successfully"
                    }, status=status.HTTP_201_CREATED)
            except Hotel.DoesNotExist:
                return Response({
                    "code": 120,
                    "message": "hotel does not exist",
                    "resolve": "Incorrect hotel id"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)