from django.db import models

# Create your models here.

class Vendor(models.Model):
    """Add unique = True to the field name to prevent duplicate values"""
    vendor_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.vendor_name

class Subscription(models.Model):
    subscription_name = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.subscription_name
