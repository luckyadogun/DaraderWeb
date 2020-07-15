from django import forms

from .models import Hotel, HotelPhotos, Room, FAQ, HotelBookingRequest

class HotelBookingRequestForm(forms.ModelForm):

    class Meta:
        model = HotelBookingRequest
        fields = ['comment', 'mobile_phone']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'contact-form__textarea mb-25', 'cols': 10,
                'placeholder': 'Enter your message',
                'required': True}),
            'mobile_phone': forms.TextInput(attrs={
                'class': 'form-control filter-input', 
                'placeholder': 'Enter your phone number',
                'required': True})
        }

class HotelPhotosForm(forms.ModelForm):
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={
            'multiple': True, 'class': 'add-listing__input-file',
            'type': 'file', 'name': 'file', 'id': 'img_file'}))

    class Meta:
        model = HotelPhotos
        exclude = ('hotel',)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ('hotel',)
        widgets = {
            'room_name': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter room name',
                'required': 'true'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter the room price'}),
            'information': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the room description',
                'rows': 3
            })
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        exclude = ('hotel',)
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter the question',
                'required': 'true'}),
            'answer': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter the answer',
                'required': 'true'}),
        }


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        exclude = ('creator',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter the Hotel name',
                'required': 'true'}),
            'average_price': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter the average room price'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the hotel address',
            }),
            'hotel_type': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select',
                'name': 'hotel_type'}),
            'number_of_rooms': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter the number of rooms'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the hotel',
            }),
            'has_restaurant': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-a'}),
            'has_bar': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-b'}),
            'has_wireless_internet': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-c'}),
            'has_24_hrs_electricity': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-d'}),
            'has_adequate_parking_space': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-e'}),
            'has_swimming_pool': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-f'}),
            'has_car_rental': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-g'}),
            'has_double_bed': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-h'}),
            'has_toiletries': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-i'}),
            'has_concierge': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-j'}),
            'has_shower': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-k'}),
            'has_room_service': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-l'}),
            'has_key_card_system': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-m'}),
            'has_gym': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-n'}),
            'has_airport_pickup': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-o'}),
            'has_car_hire': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-p'}),
            'has_laundry': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-q'}),
            'has_spa_treatment': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-r'}),
            'has_night_club': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-s'}),
            'has_luggage_storage': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-t'}),
            'has_air_conditioning': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-u'}),
            'has_car_wash': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-v'})            
        }

class HotelUpdateForm(HotelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = self.instance.name
        self.fields['address'].widget.attrs['placeholder'] = self.instance.address
        # self.fields['number_of_rooms'].widgets.attrs['placeholder'] = self.instance.number_of_rooms
        self.fields['hotel_type'].widget.attrs['value'] = self.instance.hotel_type
        self.fields['average_price'].widget.attrs['placeholder'] = self.instance.average_price
        self.fields['description'].widget.attrs['placeholder'] = self.instance.description


class HotelPhotosUpdateForm(HotelPhotosForm):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['required'] = False