from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError

from groups_custumer.models import GroupsClass
from custumer.models import SportCategory, Custumer
from authen.models import Gender 


@login_required
def customer_list(request):
    context= {}
    search_query = request.GET.get('search', '')
    group_filter = request.GET.get('group', '')
    gender_filter = request.GET.get('gender', '')
    birth_year_filter = request.GET.get('birth_year', '')

    customers = Custumer.objects.filter(owner=request.user).order_by('id')

    if search_query:
        customers = customers.filter(
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    if group_filter:
        customers = customers.filter(groups__id__in=[group_filter])
    
    if gender_filter:
        customers = customers.filter(gender=gender_filter)
    
    if birth_year_filter:
        customers = customers.filter(birth_date__year=birth_year_filter)
    context['groups'] = GroupsClass.objects.filter(owner_id=request.user)
    context['gender'] = Gender.objects.all()
    context['custumer'] = customers

    return render(request, 'customer/crud/index.html', context)


@login_required
def customer_create(request):
    context = {}
    context['gender'] = Gender.objects.all()
    context['groups'] = GroupsClass.objects.filter(owner_id=request.user)
    context['sport_category'] = SportCategory.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        gender_id = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        email = request.POST.get('email')
        contract_number = request.POST.get('contract_number')
        contract_type = request.POST.get('contract_type')
        start_date = request.POST.get('start_date')
        group_ids = request.POST.getlist('group')
        sport_category_id = request.POST.get('sport_rank')
        photo = request.FILES.get('photo')
        context.update({
            'form_data': {
                'full_name': full_name,
                'phone': phone,
                'gender': gender_id,
                'birth_date': birth_date,
                'address': address,
                'email': email,
                'contract_number': contract_number,
                'contract_type': contract_type,
                'start_date': start_date,
                'group': group_ids,
                'sport_rank': sport_category_id
            },
            'errors': []
        })
        if not full_name or not phone or not gender_id or not birth_date or not address or not email or not contract_number or not contract_type or not start_date:
            context['error'] = "Заполнение требуемой информации является обязательным."
            return render(request, 'customer/crud/create.html', context)

        try:
            gender = Gender.objects.get(id=gender_id) if gender_id else None
            sport_category = SportCategory.objects.get(id=sport_category_id) if sport_category_id else None

            customer = Custumer(
                full_name=full_name,
                phone=phone,
                gender=gender,
                birth_date=birth_date,
                address=address,
                email=email,
                contract_number=contract_number,
                contract_type=contract_type,
                strat_date=start_date,
                sport_category=sport_category,
                photo=photo,
                owner=request.user
            )
            customer.full_clean()
            customer.save()

            if group_ids:
                groups = GroupsClass.objects.filter(id__in=group_ids, owner_id=request.user)
                customer.groups.set(groups)

            return redirect('customer_list')

        except ValidationError as e:
            for field, error_list in e.message_dict.items():
                for error in error_list:
                    context['errors'].append(f"Ошибка в поле '{field}': {error}")
        except Exception as e:
            context['errors'].append(f"Произошла ошибка: {str(e)}")

    return render(request, 'customer/crud/create.html', context)


@login_required
def custumer_update(request, pk):
    context = {}
    context['gender'] = Gender.objects.all()
    context['groups'] = GroupsClass.objects.filter(owner_id=request.user)
    context['sport_categorys'] = SportCategory.objects.all()
    context['custumer'] = Custumer.objects.filter(id=pk)[0]

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        gender_id = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        email = request.POST.get('email')
        contract_number = request.POST.get('contract_number')
        contract_type = request.POST.get('contract_type')
        start_date = request.POST.get('start_date')
        group_ids = request.POST.getlist('group')
        sport_rank_id = request.POST.get('sport_rank')
        
        photo = request.FILES.get('photo')

        if not all([full_name, phone, gender_id, birth_date, address, email, contract_number, contract_type, start_date, sport_rank_id]):
            context['error'] = "Заполните все обязательные поля!"
            return render(request, 'customer/crud/update.html', context)

        gender = Gender.objects.get(id=gender_id)
        sport_category = SportCategory.objects.get(id=sport_rank_id) if sport_rank_id else None

        context['custumer'].full_name = full_name
        context['custumer'].phone = phone
        context['custumer'].gender = gender
        context['custumer'].birth_date = birth_date
        context['custumer'].address = address
        context['custumer'].email = email
        context['custumer'].contract_number = contract_number
        context['custumer'].contract_type = contract_type
        context['custumer'].strat_date = start_date
        context['custumer'].sport_category = sport_category

        if photo:
            context['custumer'].photo = photo

        context['custumer'].groups.set(group_ids)
        context['custumer'].save()
        return redirect('customer_list')

    return render(request, 'customer/crud/update.html', context)


@login_required
def cutsumer_detaile(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    
    return render(request, 'customer/crud/detaile.html', context)


@login_required
def cutsumer_delete(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    context['cutumer'].delete()
    return redirect('customer_list')
