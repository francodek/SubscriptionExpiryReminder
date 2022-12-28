from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #import Paginator
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm


# Create your views here.
"""""
def indexView(request):
    SubscriptionListView = Subscription.objects.all()  # queryset containing all movies we just created
    paginator = Paginator(SubscriptionListView, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #return render(request=request, template_name="main/movies.html", context={'movies': page_obj})

    return render(request, 'index.html',context={'SubscriptionListView': page_obj})
"""""
now = timezone.now()
def indexView(request):
    subscription_list  = SubscriptionListView.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(subscription_list, 5)
    try:
        Subscription = paginator.page(page)
    except PageNotAnInteger:
        Subscription = paginator.page(1)
    except EmptyPage:
        Subscription = paginator.page(paginator.num_pages)

    return render(request, 'core/user_list.html', { 'Subscription': Subscription })



@method_decorator(login_required, name='dispatch')
class SubscriptionListView(ListView):
    template_name = 'subscriptionlist.html'
    context_object_name = 'subscription_list'
    model = Subscription
    paginate_by = 5
    queryset = Subscription.objects.all()  # Default: Model.objects.all()

    def get_queryset(self):
        return Subscription.objects.all()




@method_decorator(login_required, name='dispatch')
class VendorListView(ListView):
    template_name = 'vendorlist.html'
    context_object_name = 'vendor_list'

    def get_queryset(self):
        return Vendor.objects.all()

@login_required()
def expiringsublist(request):
    no_of_days = request.GET.get('days_left')
    if no_of_days is not None:
        days_left = int(no_of_days)
        expired_subscription_list = Subscription.objects.filter(expiry_date__gte=now.date(),
                                                                expiry_date__exact=now.date() + timedelta(days=days_left))

        return render(request, 'expired_subscriptionlist.html',
                      {'expired_subscription_list': expired_subscription_list})
    expired_subscription_list = Subscription.objects.filter(expiry_date__gte=now.date(),
                                                            expiry_date__exact=now.date() + timedelta(days=1))
    return render(request, 'expired_subscriptionlist.html', {'expired_subscription_list': expired_subscription_list})

def send_email(request):
    if request.method == 'POST':
        form = request.POST
        expired_subscription_list = Subscription.objects.filter(expiry_date__gte=now.date(),
                                                                expiry_date__exact=now.date() + timedelta(days=1))
        for subscription in expired_subscription_list:
            if subscription is not None:
                subject = "Expriy notification"
                message = f"Your Subscription, {subscription.subscription_name} will be expiring on {subscription.expiry_date}"
                #to = form.cleaned_data['to']
                send_mail(subject, message, 'francisopogah@gmail.com', ['francisopogah45@gmail.com', subscription.email])
        return redirect('expired_subscription_list')

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = CustomUserCreationForm()
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
    vendor = get_object_or_404(Vendor, pk=pk)
    form = VendorForm(request.POST or None, instance=vendor)
    if form.is_valid():
        form.save()
        return redirect('vendor_list')
    return render(request, 'edit_vendor.html', {'form': form})


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
            sub_name = form.cleaned_data.get("subscription_name")
            vendor = form.cleaned_data.get("vendor")
            date_subscribed = form.cleaned_data.get("date_subscribed")
            expiry_date = form.cleaned_data.get("expiry_date")
            email = form.cleaned_data.get("email")
            # process the data in form.cleaned_data as required
            # ...
            subject = "Subscription Notification"
            message = f"Hello, \nYou have successfully subscribed for {sub_name} from " \
                      f"{vendor} \nDate Subscribed - {date_subscribed} \nExpiration Date - {expiry_date}"
            send_mail(subject, message, 'francisopogah@gmail.com', {email})
            # redirect to a new URL:
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()

    return render(request, 'createsubscription.html', {'form': form})


def editsubscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    form = SubscriptionForm(request.POST or None, instance=subscription)
    if form.is_valid():
        form.save()
        return redirect('subscription_list')
    return render(request, 'edit_subscription.html', {'form': form})


def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'delete_subscription.html', {'subscription': subscription})

# class based views

