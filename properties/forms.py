from django import forms

from properties.models import BookingRequest

DATE_INPUT_FORMATS = ['%Y-%m-%d',]
TIME_INPUT_FORMATS = ['%I:%M %p',]


class BookingRequestForm(forms.ModelForm):
    tour_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    tour_time = forms.TimeField(input_formats=TIME_INPUT_FORMATS)

    class Meta:
        model = BookingRequest
        fields = [
            'tour_date', 'tour_time',
            'comment', 'mobile_phone']
        widgets = {
            'tour_date': forms.DateInput(attrs={
                'class': 'form-control', 'required': True}),
            'tour_time': forms.TimeInput(attrs={
                'class': 'listing-input hero__form-input  form-control custom-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'contact-form__textarea mb-25', 'cols': 10}),
            'mobile_phone': forms.TextInput(attrs={
                'class': 'form-control filter-input'})
        }