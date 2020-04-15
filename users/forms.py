from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from properties.models import (
    Property, PropertyDetails,
    Country, State, Company, Gallery)

from .models import User
from .utils import validate_phone


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Included all the
    required fields, plus a repeat password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2  = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(
        label="Internal Staff", 
        widget=forms.CheckboxInput,
        required=False)
    is_account_manager = forms.BooleanField(
        label="Account Manager",
        widget=forms.CheckboxInput,
        required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'is_staff', 'is_account_manager')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is taken!")
        if username.lower() == "admin":
            raise forms.ValidationError("Unauthorized username!")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)    
    mobile_phone = forms.CharField(
        max_length=20, 
        validators=[validate_phone],
        required=False)
    facebook = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    instagram = forms.URLField(required=False)
    # password = ReadOnlyPasswordHashField
    is_staff = forms.BooleanField(
        label="Internal Staff", 
        widget=forms.CheckboxInput,
        required=False)
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=False)
    is_account_manager = forms.BooleanField(
        label="Account Manager",
        widget=forms.CheckboxInput,
        required=False)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 
            'is_active', 'is_staff', 'first_name',
            'last_name', 'mobile_phone', 
            'is_account_manager')

    def clean_password(self):
        return self.initial["password"]


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        exclude = ('slug', 'owner', 'market_status',)
        widgets = {
            'property_id': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'readonly': 'readonly'}),

            'title': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter property title',
                'required': 'true'}),

            'address': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter property address',
                'required': 'true'}),

            'area': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter Neighborhood'}),

            'country': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select'}),

            'state': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select'}),

            'zipcode': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '(Optional) Enter Zipcode'}),

            'property_type': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select'}),

            'property_category': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select'}),

            'price': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '3000000', 'required': 'true'}),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a property description',
                'required': 'true'}),
        }

    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.fields['owner'] = forms.ModelChoiceField(
    #         queryset=Company.objects.filter(manager__id=1))


class GalleryForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={
            'multiple': True, 'class': 'add-listing__input-file',
            'type': 'file', 'name': 'file', 'id': 'img_file'}))

    class Meta:
        model = Gallery
        exclude = ('property_obj',)


class PropertyDetailsForm(forms.ModelForm):

    class Meta:
        model = PropertyDetails
        exclude = ('property_obj',)
        widgets = {
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter number of bedrooms'}),

            'livingrooms': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter number of living rooms'}),

            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter number of bathrooms'}),

            'toilets': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '(Optional) Enter number of toilets'}),

            'parking_spaces': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter number of parking spaces'}),

            'total_area': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '(Optional) Enter property total area'}),

            'covered_area': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '(Optional) Enter property occupied area'}),

            'has_basketball_court': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-a'}),

            'has_gym': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-b'}),

            'is_wheelchair_friendly': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-c'}),

            'has_swimming_pool': forms.CheckboxInput(attrs={
                'class': 'form-control filter-input', 'id': 'check-d'}),
        }


class PropertyUpdateForm(PropertyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property_id'].widget.attrs['placeholder'] = self.instance.property_id
        self.fields['title'].widget.attrs['placeholder'] = self.instance.title
        self.fields['address'].widget.attrs['placeholder'] = self.instance.address
        self.fields['area'].widget.attrs['placeholder'] = self.instance.area
        self.fields['country'].widget.attrs['value'] = self.instance.country
        self.fields['state'].widget.attrs['value'] = self.instance.state
        self.fields['zipcode'].widget.attrs['placeholder'] = self.instance.zipcode
        self.fields['property_type'].widget.attrs['value'] = self.instance.property_type
        self.fields['property_category'].widget.attrs['value'] = self.instance.property_category
        self.fields['price'].widget.attrs['placeholder'] = self.instance.price
        self.fields['description'].widget.attrs['placeholder'] = self.instance.description


class DetailsUpdateForm(PropertyDetailsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bedrooms'].widget.attrs['placeholder'] = self.instance.bedrooms
        self.fields['livingrooms'].widget.attrs['placeholder'] = self.instance.livingrooms
        self.fields['bathrooms'].widget.attrs['placeholder'] = self.instance.bathrooms
        self.fields['toilets'].widget.attrs['placeholder'] = self.instance.toilets        
        self.fields['parking_spaces'].widget.attrs['placeholder'] = self.instance.parking_spaces
        self.fields['total_area'].widget.attrs['placeholder'] = self.instance.total_area
        self.fields['covered_area'].widget.attrs['placeholder'] = self.instance.covered_area
