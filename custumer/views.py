from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def customer_list(request):
    return render(request, 'customer/crud/index.html')


@login_required
def customer_create(request):
    return render(request, 'customer/crud/create.html')