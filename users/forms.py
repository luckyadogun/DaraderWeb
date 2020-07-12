from django import forms

from properties.models import (
    Property, PropertyDetails, 
    Gallery, Company, State, LGA,
    FloorPlan)

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
    first_name = forms.CharField(
        label='First Name',
        max_length=200,
        required=False)
    last_name = forms.CharField(
        label='Last Name',
        max_length=200,
        required=False)
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


class AccountUpdateForm(forms.ModelForm):
    old_password = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control filter-input', 'placeholder': 'Enter old password'}))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control filter-input', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control filter-input', 'placeholder': 'Enter new password again'}))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'mobile_phone',
            'facebook', 'twitter',
            'instagram'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'First Name',
                'required': False}),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Last Name',
                'required': False}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Email address',
                'required': False}),
            'mobile_phone': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '+2348123456789',
                'required': False}),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Facebook URL (Optional)',
                'required': False}),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Twitter URL (Optional)',
                'required': False}),
            'instagram': forms.URLInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Instagram URL (Optional)',
                'required': False}),
        }

        def clean_new_password2(self):
            old_password = self.cleaned_data.get("old_password")
            new_password = self.cleaned_data.get("new_password")
            new_password2 = self.cleaned_data.get("new_password2")

            if old_password and new_password and new_password2:
                if new_password != new_password2:
                    raise forms.ValidationError("Passwords don't match!")
            return new_password2


class CompanyForm(forms.ModelForm):
    logo = forms.ImageField(required=True, widget=forms.ClearableFileInput(
        attrs={
            'class': 'add-listing__input-file', 
            'name': 'file', 'type': 'file'}))

    class Meta:
        model = Company
        fields = (
            'name', 'office_phone',
            'mobile_phone', 'address',
            'logo', 'about', 'account_type'
            )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Company Name',
                'required': True}),
            'office_phone': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '+2348123456789',
                'required': False}),
            'mobile_phone': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': '+2348123456789',
                'required': False}),
            'address': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Company Address',
                'required': True}),
            'about': forms.Textarea(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Tell us about your company',
                'required': True}),
            'account_type': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select'}),            
        }


class CompanyUpdateForm(CompanyForm):    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = self.instance.name
        self.fields['office_phone'].widget.attrs['placeholder'] = self.instance.office_phone
        self.fields['mobile_phone'].widget.attrs['placeholder'] = self.instance.mobile_phone
        self.fields['address'].widget.attrs['placeholder'] = self.instance.address
        self.fields['about'].widget.attrs['placeholder'] = self.instance.about
        self.fields['account_type'].widget.attrs['placeholder'] = self.instance.account_type
        self.fields['logo'].widget.attrs['required'] = False


class PropertyForm(forms.ModelForm):
    lga = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'listing-input hero__form-input form-control custom-select'}), 
        queryset=LGA.objects.none(), required=False)

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

            'country': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select',
                'name': 'country'}),

            'state': forms.Select(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select',
                'name': 'state'}),            

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


class GalleryForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={
            'multiple': True, 'class': 'add-listing__input-file',
            'type': 'file', 'name': 'file', 'id': 'img_file'}))

    class Meta:
        model = Gallery
        exclude = ('property_obj',)


class FloorPlanForm(forms.ModelForm):
    floor_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={
            'multiple': False, 'class': 'add-listing__input-file',
            'type': 'file', 'name': 'file', 'id': 'floorplan_file'}))

    class Meta:
        model = FloorPlan
        exclude = ('property_obj',)
        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter floor title',
                'required': 'true'}),

            'size': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter size of property'}),

            'rooms': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter size of rooms'}),

            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control filter-input',
                'placeholder': 'Enter size of bathrooms'}),
        }


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
                'placeholder': 'Enter property occupied area - (Limit:32767)'}),

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
        self.fields['lga'].widget.attrs['placeholder'] = self.instance.lga
        self.fields['country'].widget.attrs['value'] = self.instance.country
        self.fields['state'].widget.attrs['value'] = self.instance.state
        self.fields['zipcode'].widget.attrs['placeholder'] = self.instance.zipcode
        self.fields['property_type'].widget.attrs['value'] = self.instance.property_type
        self.fields['property_category'].widget.attrs['value'] = self.instance.property_category
        self.fields['price'].widget.attrs['placeholder'] = self.instance.price
        self.fields['description'].widget.attrs['placeholder'] = self.instance.description


class GalleryUpdateForm(GalleryForm):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['required'] = False


class FloorPlanUpdateForm(FloorPlanForm):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['floor_image'].widget.attrs['required'] = False
        self.fields['title'].widget.attrs['required'] = False
        self.fields['size'].widget.attrs['placeholder'] = self.instance.size
        self.fields['rooms'].widget.attrs['placeholder'] = self.instance.rooms
        self.fields['bathrooms'].widget.attrs['placeholder'] = self.instance.bathrooms


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