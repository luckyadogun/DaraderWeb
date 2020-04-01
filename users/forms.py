from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Included all the
    required fields, plus a repeat password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2  = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(
        label="Internal Staff", 
        widget=forms.CheckboxInput,
        required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'is_staff')

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
    password = ReadOnlyPasswordHashField
    is_staff = forms.BooleanField(
        label="Internal Staff", 
        widget=forms.CheckboxInput,
        required=False)
    is_active = forms.BooleanField(widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]