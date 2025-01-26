from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from groups_custumer.models import GroupsClass
from custumer.models import Custumer, CustumerRepresentatives, TypeRepresentatives


@login_required
def custumer_representatives_all(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    context['objects_list'] = CustumerRepresentatives.objects.filter(custumer=context['cutumer'])

    return render(request, 'customer/representatives/index.html', context)


@login_required
def custumer_representatives_create(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    context['objects_list'] = TypeRepresentatives.objects.all()

    if request.method == 'POST':
        type_id = request.POST.get('type')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        work = request.POST.get('work')

        if not type_id or not full_name or not phone:
            context['error'] = 'Все обязательные поля должны быть заполнены.'
            context['form_data'] = {
                'full_name': full_name,
                'phone': phone,
                'work': work
            }
            return render(request, 'customer/representatives/create.html', context)

        try:
            type_obj = TypeRepresentatives.objects.get(id=type_id)
        except TypeRepresentatives.DoesNotExist:
            context['error'] = 'Указанный тип родства не найден.'
            context['form_data'] = {
                'full_name': full_name,
                'phone': phone,
                'work': work
            }
            return render(request, 'customer/representatives/create.html', context)

        CustumerRepresentatives.objects.create(
            type=type_obj,
            full_name=full_name,
            phone=phone,
            work=work,
            custumer=context['cutumer']
        )
        return redirect('custumer_representatives_all', pk=pk)

    return render(request, 'customer/representatives/create.html', context)



@login_required
def custumer_representatives_delete(request, customer_id, representative_id):
    # Obyektlarni olish
    custumer = get_object_or_404(Custumer, id=customer_id)
    representative = get_object_or_404(CustumerRepresentatives, id=representative_id, custumer=custumer)
    representative.delete()
    return redirect('custumer_representatives_all', customer_id)