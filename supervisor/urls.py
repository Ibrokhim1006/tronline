from django.urls import path
from supervisor.views import supervisor_home


urlpatterns = [
    path('cabinet/', supervisor_home, name='cabinet'),

]