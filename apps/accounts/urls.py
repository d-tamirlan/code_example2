from django.contrib import admin
from django.urls import path, include
from .views import UserRegistrationView, TransactionView


app_name = 'accounts'


urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
]
