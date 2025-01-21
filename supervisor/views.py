from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def supervisor_home(request):
    return render(request, 'supervisor/index.html')