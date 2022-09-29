from django import forms
from django.forms import ModelForm

from .models import *

class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

