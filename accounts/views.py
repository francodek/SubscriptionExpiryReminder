from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
# Create your views here.

def indexView(request):
    return render(request,'index.html')

@method_decorator(login_required, name='dispatch')
class SubscriptionListView(ListView):
	template_name='subscriptionlist.html'
	context_object_name = 'subscription_list'
	def get_queryset(self):
		return Subscription.objects.all()

@method_decorator(login_required, name='dispatch')
class VendorListView(ListView):
	template_name='vendorlist.html'
	context_object_name = 'vendor_list'
	def get_queryset(self):
		return Vendor.objects.all()



"""@login_required
def dashboardview(request):
    Subscriptions = Subscription.objects.all()

    form = SubscriptionForm()

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('')
    context = {'Subscriptions': Subscriptions,'form': form}
    return render(request,'dashboard.html',context)
    """

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def create_vendor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VendorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            form.save()
            # redirect to a new URL:
            return redirect('vendor_list')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VendorForm()

    return render(request, 'create.html', {'form': form})

def edit(request, pk):
    vendor= get_object_or_404(Vendor, pk=pk)
    form = VendorForm(request.POST or None, instance=vendor)
    if form.is_valid():
        form.save()
        return redirect('vendor_list')
    return render(request, 'edit_vendor.html', {'form':form})

"""""
def delete_vendor(request, pk, vendor_id):
    vendor_id = int(vendor_id)
    try:
        vendor_sel = Vendor.objects.get( id = vendor_id)
    except Vendor.DoesNotExist:
        return redirect('vendor_list')
    vendor_sel.delete()
    return redirect(request,'vendor_list')
"""""

def delete_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendor_list')
    return render(request, 'delete_vendor.html', {'vendor': vendor})

def create_subscription(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            form.save()
            # redirect to a new URL:
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()

    return render(request, 'createsubscription.html', {'form': form})


def editsubscription(request, pk):
    subscription= get_object_or_404(Subscription, pk=pk)
    form = SubscriptionForm(request.POST or None, instance=subscription)
    if form.is_valid():
        form.save()
        return redirect('subscription_list')
    return render(request, 'edit_subscription.html', {'form':form})

def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'delete_subscription.html', {'subscription': subscription})