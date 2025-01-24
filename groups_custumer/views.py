from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from groups_custumer.models import Week, TypeSports, GroupsClass, Schedule
from authen.models import CustomUser
from employe.models import Employe


@login_required
def gorups_all(request):
    search_query = request.GET.get('search', '')
    employe_id = request.GET.get('employe_id', '')
    groups_qs = GroupsClass.objects.filter(owner_id=request.user).order_by('-id')

    if search_query:
        groups_qs = groups_qs.filter(
            Q(name__icontains=search_query) | 
            Q(strat_training__icontains=search_query)
        )

    if employe_id:
        groups_qs = groups_qs.filter(employe_id=employe_id)

    context = {
        'employes': Employe.objects.filter(owner=request.user).order_by('-id'),
        'groups': groups_qs,
        'search_query': search_query,
        'selected_employe_id': employe_id,
    }
    return render(request, 'groups/index.html', context)


@login_required
def groups_create(request):
    context = {}
    context['employes'] = Employe.objects.filter(owner=request.user).order_by('-id')
    context['weeks'] = Week.objects.all()
    context['type_sports'] = TypeSports.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        sport_type_id = request.POST.get('sport_type')
        coaches = request.POST.getlist('coaches')
        start_date = request.POST.get('start_date')
        position = request.POST.get('position')
        weeks_data = request.POST.getlist('weeks[]')
        time_strat = request.POST.getlist('time_strat')
        time_end = request.POST.getlist('time_end')

        # Check required fields
        if not name or not sport_type_id or not coaches or not start_date or not position:
            context['error'] = "Все поля обязательны для заполнения, за исключением полей «Неделя» и «Время»."
            return render(request, 'groups/create.html', context)

        # Convert sport_type_id to the TypeSports instance
        try:
            sport_type = TypeSports.objects.get(id=sport_type_id)
        except TypeSports.DoesNotExist:
            context['error'] = "Указанный вид спорта не существует."
            return render(request, 'groups/create.html', context)

        # Create the group
        group = GroupsClass.objects.create(
            name=name,
            type_sport=sport_type,
            strat_training=start_date,
            position=position,
            owner_id=request.user
        )

        # Add selected coaches to the group
        coaches_objs = Employe.objects.filter(id__in=coaches)
        group.employe_id.add(*coaches_objs)

        # Add schedule for the group
        for week, start_time, end_time in zip(weeks_data, time_strat, time_end):
            if week and start_time and end_time:
                Schedule.objects.create(
                    groups_id=group,
                    week_id=week,
                    strat_time=start_time,
                    end_time=end_time
                )

        return redirect('gorups_all')
    return render(request, 'groups/create.html', context)


@login_required
def groups_update(request, pk):
    context = {}
    context['groups'] = GroupsClass.objects.filter(id=pk)[0]
    context['employes'] = Employe.objects.filter(owner=request.user).order_by('-id')
    context['weeks'] = Week.objects.all()
    context['type_sports'] = TypeSports.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        sport_type_id = request.POST.get('sport_type')
        coaches_ids = request.POST.getlist('coaches')
        start_date = request.POST.get('start_date')
        position = request.POST.get('position')
        schedules = request.POST.getlist('weeks[]')
        start_times = request.POST.getlist('time_strat')
        end_times = request.POST.getlist('time_end')

        # Yangi ma'lumotlarni yangilash
        if not name or not sport_type_id or not coaches_ids or not start_date or not position:
            context['error'] = "Все поля обязательны для заполнения, за исключением полей «Неделя» и «Время»."
            return render(request, 'groups/update.html', context)

        try:
            try:
                sport_type = TypeSports.objects.get(id=sport_type_id)
            except TypeSports.DoesNotExist:
                context['error'] = "Указанный вид спорта не существует."
                return render(request, 'groups/create.html', context)
            context['groups'].name = name
            context['groups'].type_sport = sport_type
            context['groups'].strat_training = start_date
            context['groups'].position = position
            context['groups'].save()

            # Trenerlar bilan bog'lash
            context['groups'].employe_id.set(coaches_ids)

            # Eski jadvalni tozalash
            context['groups'].groups.all().delete()
            # Yangi jadvalni saqlash
            for week_id, start_time, end_time in zip(schedules, start_times, end_times):
                if week_id and start_time and end_time:
                    week = Week.objects.get(id=week_id) 
                    context['groups'].groups.create(
                        week=week,
                        strat_time=start_time,
                        end_time=end_time
                    )
        
            return redirect('gorups_all')

        except Exception as e:
            context['error'] = f"Произошла ошибка: {str(e)}"
            return render(request, 'groups/update.html', context)

    return render(request, 'groups/update.html', context)