from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from authen.models import CustomUser


def sign_in(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "" or password == "":
            context["error"] = "Логин или пароль пуст !"
            return render(request, "authen/login.html", context)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if len(user.groups.all().filter(name="admin")) != 0:
                return redirect("cabinet")
            else:
                context["error"] = "Доступ к этой системе запрещен !"
                return render(request, "authen/login.html", context)
        else:
            context["error"] = "неверный логин или пароль !"
    return render(request, "authen/login.html", context)


def sign_up(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        # Bo'sh maydonlarni tekshirish
        if not all([name, email, phone, password, password2]):
            context["error"] = "Заполните информацию!"
            return render(request, "authen/register.html", context)
        
        # Parolni tasdiqlash
        if password != password2:
            context["error"] = "Пароли не совпадают. Попробуйте еще раз."
            return render(request, "authen/register.html", context)
        
        # Email va telefon mavjudligini tekshirish
        if CustomUser.objects.filter(email=email).exists():
            context["error"] = "Этот e-mail уже занят. Пожалуйста, выберите другой."
            return render(request, "authen/register.html", context)
        if CustomUser.objects.filter(phone=phone).exists():
            context["error"] = "Этот телефон уже занят. Пожалуйста, выберите другой."
            return render(request, "authen/register.html", context)
        
        # Foydalanuvchini yaratish
        try:
            user = CustomUser.objects.create(
                first_name=name,
                username=email,
                email=email,
                phone=phone,
                password=make_password(password),  # Parolni shifrlash
            )
            admin_group, created = Group.objects.get_or_create(name="admin")
            user.groups.add(admin_group)
            context["success"] = "Регистрация прошла успешно!"
            return redirect("sign_in")  # Login sahifasiga yo'naltirish
        except Exception as e:
            context["error"] = f"Ошибка при регистрации: {e}"
            return render(request, "authen/register.html", context)
    
    return render(request, 'authen/register.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect("/")
