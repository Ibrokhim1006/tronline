from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def sign_in(request):
    return render(request, 'authen/login.html')


def sign_up(request):
    return render(request, 'authen/login.html')

