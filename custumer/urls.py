from django.urls import path
from custumer.views import customer_list, customer_create


urlpatterns = [
    path('customer/all/', customer_list, name='customer_list'),
    path('customer/add/', customer_create, name='customer_create'),
    
]