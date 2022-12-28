from django import forms
from django.contrib.auth.models import User

from .models import *
from datetimepicker.widgets import DateTimePicker
from django.contrib.auth.forms import UserCreationForm


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class SubscriptionForm(forms.ModelForm):
    expiry_date = forms.DateTimeField(widget=DatePickerInput)
    date_subscribed = forms.DateTimeField(widget=DatePickerInput)

    class Meta:
        model = Subscription
        fields = '__all__'


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'





class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")