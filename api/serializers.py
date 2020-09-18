from rest_framework import serializers
from hotels.models import Hotel, Room, HotelPhotos, FAQ, BookmarkedHotel
from properties.models import Property, Gallery, FloorPlan, PropertyDetails, BookmarkedProperty, Country, State, LGA, Company
from users.models import User
from geopy.geocoders import Nominatim
from requests.exceptions import ConnectionError

# User info
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','groups','user_permissions',)

# Login and Register
class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class LGASerializer(serializers.ModelSerializer):
    class Meta:
        model = LGA
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

# Hotel Serializers related
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class HotelPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhotos
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True, many=True)
    hotelPhotos = HotelPhotosSerializer(read_only=True, many=True)
    faq = FAQSerializer(read_only=True, many=True)
    location = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = '__all__'
    def get_location(self, obj):
        print(obj.address)
        geolocator = Nominatim(user_agent="sademolaadedeji@gmail.com")
        try:
            position = geolocator.geocode(obj.address)
            return (position.latitude, position.longitude)
        except:
            return "Unable to get data"

# Proprty serializer related
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class FloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlan
        fields = '__all__'

class PropertyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    lga = LGASerializer(read_only=True)
    owner = CompanySerializer(read_only=True)
    gallery = GallerySerializer(read_only=True, many=True)
    floorplan = FloorPlanSerializer(read_only=True, many=True)
    property_details = PropertyDetailsSerializer(read_only=True, many=True)
    location = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = '__all__'    

    def get_location(self, obj):
        geolocator = Nominatim(user_agent="sademolaadedeji@gmail.com")
        try:
            position = geolocator.geocode(obj.address)
            return (position.latitude, position.longitude)
        except:
            return "Unable to get data"

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

class BookmarkedPropertySerializer(serializers.ModelSerializer):
    property_obj = PropertySerializer(read_only=True)
    # owner = UserSerializer(read_only=True)
    class Meta:
        model = BookmarkedProperty
        fields = '__all__'

class BookmarkedHotelSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    # owner = UserSerializer(read_only=True)
    class Meta:
        model = BookmarkedHotel
        fields = '__all__'
    