from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.apps import apps

from employe.models import EmployeRoll


@login_required
def employe_roll(request):
    context = {}
    context['roll_list'] = EmployeRoll.objects.filter(owner=request.user).order_by('-id')
    return render(request, 'roll/index.html', context)


@login_required
def employe_roll_create(request):
    context = {}
    permissions = Permission.objects.none()

    for app_config in apps.get_app_configs():
        if app_config.label in ['customer', 'employe']:
            for model in app_config.get_models():
                content_type = ContentType.objects.get_for_model(model)
                model_permissions = Permission.objects.filter(content_type=content_type)
                permissions = permissions | model_permissions
    context['permission'] = permissions

    if request.method == 'POST':
        name = request.POST.get('name')
        permission_ids = request.POST.getlist('permission')

        if not name or not permission_ids:
            context['error'] = "Заполните все обязательные поля!"
            return render(request, 'roll/create.html', context)
        
        roll = EmployeRoll(name=name, owner=request.user)
        roll.save()
        
        permissions = Permission.objects.filter(id__in=permission_ids)
        roll.permissons.set(permissions)
        
        return redirect('employe_roll')
    return render(request, 'roll/create.html', context)


@login_required
def employe_roll_update(request, pk):
    context = {}
    permissions = Permission.objects.none()

    for app_config in apps.get_app_configs():
        if app_config.label in ['customer', 'employe']:
            for model in app_config.get_models():
                content_type = ContentType.objects.get_for_model(model)
                model_permissions = Permission.objects.filter(content_type=content_type)
                permissions = permissions | model_permissions
    context['permission'] = permissions
    context['roll'] = EmployeRoll.objects.filter(id=pk)[0]

    if request.method == 'POST':
        name = request.POST.get('name')
        permission_ids = request.POST.getlist('permission')

        if not name or not permission_ids:
            context['error'] = "Заполните все обязательные поля!"
            return render(request, 'roll/update.html', context)

        context['roll'].name = name
        context['roll'].save()
        context['roll'].permissons.set(permission_ids)
        return redirect('employe_roll') 
    return render(request, 'roll/update.html', context)


@login_required
def employe_roll_delete(request, pk):
    roll = EmployeRoll.objects.get(id=pk)
    roll.delete()
    return redirect('employe_roll')