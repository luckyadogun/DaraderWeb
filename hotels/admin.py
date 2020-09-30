from django.contrib import admin

from .models import Hotel, Room, HotelPhotos, FAQ

class HotelImageInline(admin.TabularInline):
    model = HotelPhotos
    extra = 0

class RoomInline(admin.StackedInline):
    model = Room
    extra = 0

class FaqInline(admin.StackedInline):
    model = FAQ
    extra = 0

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name','average_price','address','hotel_type','number_of_rooms','description','has_restaurant',
    'has_bar','has_wireless_internet','has_24_hrs_electricity','has_adequate_parking_space','has_swimming_pool',
    'has_car_rental','has_double_bed','has_toiletries','has_concierge','has_shower','has_room_service',
    'has_key_card_system','has_gym','has_airport_pickup','has_car_hire','has_laundry','has_spa_treatment',
    'has_night_club', 'has_luggage_storage','has_air_conditioning','has_car_wash', 'state', 'lga', 'country',)
    inlines = [HotelImageInline, RoomInline, FaqInline]
    list_filter = ('number_of_rooms',)
    search_fields = ('name',)