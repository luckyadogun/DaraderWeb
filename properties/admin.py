from django.contrib import admin

from .models import Property, \
    Company, Country, State, Gallery, \
    PropertyDetails, LGA


class PropertyDetailsInline(admin.StackedInline):
    model = PropertyDetails
    extra = 1
    max_num = 1


class PropertyImageInline(admin.TabularInline):
    model = Gallery
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    readonly_fields = ('property_id',)
    list_display = (
        'property_id', 'title', 'property_category',
        'market_status', 'price', 'owner',)    
    empty_value_display = '-empty-'
    inlines = [PropertyImageInline, PropertyDetailsInline, ]
    list_filter = ('created', 'market_status', 'property_category',)
    search_fields = ('property_id', 'owner', )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'address', 'office_phone', 
        'account_type', 'is_approved', 'is_featured',)  
    list_filter = ('created', 'is_approved', 'is_featured',) 
    search_fields = ('name', 'phone', )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country',)


@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ('name', 'state',)    