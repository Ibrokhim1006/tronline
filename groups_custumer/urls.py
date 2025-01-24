from django.urls import path
from groups_custumer.views import gorups_all, groups_create, groups_update


urlpatterns = [
    path('groups/all/', gorups_all, name='gorups_all'),
    path('groups/add/', groups_create, name='gorups_create'),
    path('groups/update/<int:pk>/', groups_update, name='groups_update'),

]