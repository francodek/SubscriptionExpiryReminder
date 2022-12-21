from django import forms
from .models import *
from datetimepicker.widgets import DateTimePicker


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


class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)