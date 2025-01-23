import secrets
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from authen.models import Gender, CustomUser
from employe.models import Employe, EmployeRoll


@login_required
def employe_list(request):
    query = request.GET.get('search', '')  # Qidiruv qiymatini olish
    employe_list = Employe.objects.filter(owner=request.user)

    if query:
        employe_list = employe_list.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(user__email__icontains=query) |
            Q(roll__name__icontains=query)
        )

    context = {
        'employe_list': employe_list.order_by('-id'),  # Saralash
        'search_query': query,  # Qidiruv qiymatini shablonda ko‘rsatish uchun
    }
    return render(request, 'employe/index.html', context)


@login_required
def employe_create(request):
    context = {}
    context['gender'] = Gender.objects.all().order_by('-id')
    context['roll'] = EmployeRoll.objects.filter(owner=request.user).order_by('-id')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        decription = request.POST.get('decription')
        roll_id = request.POST.get('roll')
        gender_id = request.POST.get('gender')

        if not full_name or not phone or not gender_id or not roll_id:
            context['error'] = "Заполните все обязательные поля!"
            return render(request, 'employe/create.html', context)

        gender_obj = get_object_or_404(Gender, id=gender_id)
        rol_obj = get_object_or_404(EmployeRoll, id=roll_id)

        if Employe.objects.filter(Q(phone=phone)).exists():
            context['error'] = "Номер телефона уже зарегистрирован."
            return render(request, 'employe/create.html', context)

        Employe.objects.create(
            full_name=full_name,
            phone=phone,
            decription=decription,
            gender=gender_obj,
            roll = rol_obj,
            owner = request.user
        )
        return redirect('employe_list')
    return render(request, 'employe/create.html', context)


@login_required
def employe_update(request, pk):
    context = {}
    context['employe'] = Employe.objects.filter(id=pk)[0]
    context['gender'] = Gender.objects.all().order_by('-id')
    context['roll'] = EmployeRoll.objects.filter(owner=request.user).order_by('-id')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        decription = request.POST.get('decription')
        gender_id = request.POST.get('gender')
        roll_id = request.POST.get('roll')

        if not full_name or not phone or not gender_id or not roll_id:
            context['error'] = "Заполните все обязательные поля!"
            return render(request, 'employe/update.html', context)
        
        if Employe.objects.filter(Q(phone=phone) & ~Q(id=pk)).exists():
            context['error'] = "Номер телефона уже зарегистрирован."
            return render(request, 'employe/update.html', context)

        gender_obj = get_object_or_404(Gender, id=gender_id)
        rol_obj = get_object_or_404(EmployeRoll, id=roll_id)

        context['employe'].full_name = full_name
        context['employe'].phone = phone
        context['employe'].decription = decription
        context['employe'].gender_id = gender_obj
        context['employe'].roll_id = rol_obj
        context['employe'].save()    

        return redirect('employe_list')

    return render(request, 'employe/update.html', context)


@login_required
def employe_delete(request, pk):
    try:
        employe = Employe.objects.get(id=pk)

        if employe.user:
            employe.user.delete()  # Faqat userni o'chirish
            employe.user = None  # Employe obyektini yangilash
            employe.is_send = False
            employe.save()       # O'zgarishlarni saqlash

        return redirect('employe_list')
    except Employe.DoesNotExist:
        # Agar employe topilmasa, sahifaga qayta yo'naltirish
        return redirect('employe_list')


@login_required
def employe_send_message(request, pk):
    context = {}
    context['employe'] = Employe.objects.filter(id=pk)[0]

    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            context['error'] = "Требуется адрес электронной почты."
            return render(request, 'employe/send_message.html', context)
        
        if CustomUser.objects.filter(Q(email=email)).exists():
            context['error'] = "E-mail уже зарегистрирован."
            return render(request, 'employe/send_message.html', context)

        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(8))
        user = CustomUser.objects.create(
                first_name=context['employe'].full_name,
                username=email,
                email=email,
                password=make_password(password)
            )
        group, created = Group.objects.get_or_create(name='assistant')
        user.groups.add(group)

        context['employe'].user = user
        context['employe'].is_send = True
        context['employe'].save()

        subject = "Ваша учетная запись создана"
        message = (
            f"Здравствуйте, {context['employe'].full_name}!\n\n"
            f"Ваша учетная запись была создана.\n"
            f"Email: {email}\n"
            f"Пароль: {password}\n\n"
            "Пожалуйста, войдите в систему, используя предоставленные учетные данные."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return redirect('employe_list')
    return render(request, 'employe/send_message.html', context)