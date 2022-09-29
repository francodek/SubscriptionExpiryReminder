from django.contrib import admin

# Register your models here.

from .models import  *

admin.site.register(Subscription)
admin.site.register(Vendor)
