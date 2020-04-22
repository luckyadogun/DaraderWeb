from django import forms

from properties.models import BookingRequest


class BookingRequestForm(forms.ModelForm):

    class Meta:
        model = BookingRequest
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


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'fname',
            'placeholder': 'Name'
        }))
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email_address',
            'placeholder': 'Email address'
        }))
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'comment',
            'placeholder': 'Your Message'
        }))
