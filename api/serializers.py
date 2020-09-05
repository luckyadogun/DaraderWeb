from rest_framework import serializers
from hotels.models import Hotel, Room, HotelPhotos, FAQ, BookmarkedHotel
from properties.models import Property, Gallery, FloorPlan, PropertyDetails, BookmarkedProperty
from users.models import User

# User info
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Login and Register
class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

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
    class Meta:
        model = Hotel
        fields = '__all__'

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
    gallery = GallerySerializer(read_only=True, many=True)
    floorplan = FloorPlanSerializer(read_only=True, many=True)
    property_details = PropertyDetailsSerializer(read_only=True, many=True)
    class Meta:
        model = Property
        fields = '__all__'

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
    