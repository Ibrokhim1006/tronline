from django.urls import path
from authen.views import sign_in, sign_up


urlpatterns = [
    path('', sign_in, name='sign_in'),
    path('regsiter/', sign_up, name='sign_up'),

]