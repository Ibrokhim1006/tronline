from django.urls import path
from custumer.views import (
    customer_list, customer_create, cutsumer_detaile,
    custumer_update, cutsumer_delete
)
from custumer.subscription.views import (
    custumer_subscriptions, custumer_subscriptions_add,
    custumer_subscriptions_update, custumer_subscriptions_detele
)
from custumer.docs.views import custumer_docs_all, custumer_dos_delet
from custumer.representatives.views import custumer_representatives_all, custumer_representatives_create, custumer_representatives_delete


urlpatterns = [
    path('customer/all/', customer_list, name='customer_list'),
    path('customer/add/', customer_create, name='customer_create'),
    path('customer/detaile/<int:pk>/', cutsumer_detaile, name='cutsumer_detaile'),
    path('customer/update/<int:pk>/', custumer_update, name='custumer_update'),
    path('customer/delete/<int:pk>/', cutsumer_delete, name='cutsumer_delete'),
    # ------ subscriptions ---
    path('customer/<int:pk>/subscriptions/', custumer_subscriptions, name='custumer_subscriptions'),
    path('customer/<int:pk>/subscriptions/create/', custumer_subscriptions_add, name='custumer_subscriptions_add'),
    path('customer/<int:custumer_id>/subscriptions/<int:sub_id>/update/', custumer_subscriptions_update, name='custumer_subscriptions_update'),
    path('customer/<int:custumer_id>/subscriptions/<int:sub_id>/delete/', custumer_subscriptions_detele, name='custumer_subscriptions_detele'),
    # Docs
    path('customer/<int:pk>/docs/', custumer_docs_all, name='custumer_docs_all'),
    path('customer/<int:custumer_id>/doc/<int:doc_id>/delete/', custumer_dos_delet, name='custumer_dos_delet'),
    # Representatives
    path('customer/<int:pk>/representatives/', custumer_representatives_all, name='custumer_representatives_all'),
    path('customer/<int:pk>/representatives/create/', custumer_representatives_create, name='custumer_representatives_create'),
    path('customers/<int:customer_id>/representatives/<int:representative_id>/delete/', custumer_representatives_delete, name='custumer_representatives_delete'),
    
]