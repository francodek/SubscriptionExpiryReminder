from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

from .views import expiringsublist, send_email

urlpatterns = [
    path('', views.indexView, name="home"),
    path('dashboard/', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('add_vendor/', views.create_vendor, name='add_vendor'),
    path('add_subscription/', views.create_subscription, name='add_subscription'),
    path('editvendor/<int:pk>/', views.edit, name='edit_vendor'),
    path('editsubscription/<int:pk>/', views.editsubscription, name='edit_subscription'),
    path('deletevendor/<int:pk>/', views.delete_vendor, name='delete_vendor'),
    path('deletesubscription/<int:pk>/', views.delete_subscription, name='delete_subscription'),
    #path('dashboard/', views.dashboardview, name="dashboard"),
    path('login/', LoginView.as_view(), name="login_url"),
    path('register/', views.registerView, name="register_url"),
    path('logout/',LogoutView.as_view(next_page='subscription_list'), name="logout"),
    path('expired/', expiringsublist, name='expired_subscription_list'),
    path('email/',send_email, name= 'send_email'),

]
