from django.urls import path
from authen.views import sign_in, sign_up, logout_user


urlpatterns = [
    path('', sign_in, name='sign_in'),
    path('regsiter/', sign_up, name='sign_up'),
    path('logout_user/', logout_user, name='logout_user')

]