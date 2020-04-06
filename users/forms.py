from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from properties.models import Property, PropertyDetails

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
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)    
    mobile_phone = forms.CharField(max_length=20, validators=[validate_phone])
    facebook = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    instagram = forms.URLField(required=False)
    # password = ReadOnlyPasswordHashField
    is_staff = forms.BooleanField(
        label="Internal Staff", 
        widget=forms.CheckboxInput,
        required=False)
    is_active = forms.BooleanField(widget=forms.CheckboxInput)
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


class PropertyUpdateForm(forms.ModelForm):
    property_obj = forms.ModelChoiceField(queryset=Property.objects.all())

    class Meta:
        model = PropertyDetails
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        property_obj = self.cleaned_data["property_obj"]
        instance.property_obj = Property.objects.get(id=property_obj)
        instance.save(commit)

        return instance
