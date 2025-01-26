from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from groups_custumer.models import GroupsClass
from custumer.models import Custumer, CustumerSubscription


@login_required
def custumer_subscriptions(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    context['subscription'] = CustumerSubscription.objects.filter(custumer=context['cutumer'])
    return render(request, 'customer/subscriptions/index.html', context)


@login_required
def custumer_subscriptions_add(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    context['groups'] = GroupsClass.objects.filter(owner_id=request.user)

    if request.method == 'POST':
        group_id = request.POST.get('group')
        number = request.POST.get('number')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        unlimited = 'unlimited' in request.POST

        if not group_id or not start_date or not end_date:
            context['error'] = 'Пожалуйста, заполните все поля!'
            return render(request, 'customer/subscriptions/create.html', context)

        if not number:
            number = None 

        group = GroupsClass.objects.get(id=group_id)
        subscription = CustumerSubscription.objects.create(
            custumer=context['cutumer'],
            groups=group,
            number_classes=number,
            start_date=start_date,
            end_date=end_date,
            unlimited=unlimited
        )
        return redirect('custumer_subscriptions', pk=context['cutumer'].id)
    return render(request, 'customer/subscriptions/create.html', context)


@login_required
def custumer_subscriptions_update(request, custumer_id, sub_id):
    context = {}
    custumer = get_object_or_404(Custumer, id=custumer_id)
    subscription = get_object_or_404(CustumerSubscription, id=sub_id)

    context['custumer'] = custumer
    context['subscription'] = subscription
    context['group'] = GroupsClass.objects.filter(owner_id=request.user)

    if request.method == 'POST':
        group_id = request.POST.get('group')
        number = request.POST.get('number')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        unlimited = 'unlimited' in request.POST

        if not group_id or not start_date or not end_date:
            context['error'] = 'Iltimos, barcha majburiy maydonlarni to\'ldiring!'
            return render(request, 'customer/subscriptions/update.html', context)

        group = get_object_or_404(GroupsClass, id=group_id)
        subscription.groups = group
        subscription.number_classes = number if number else None
        subscription.start_date = start_date
        subscription.end_date = end_date
        subscription.unlimited = unlimited
        subscription.save()

        return redirect('custumer_subscriptions', pk=custumer.id)

    context['form_data'] = {
        'group': subscription.groups.id,
        'number': subscription.number_classes,
        'start_date': subscription.start_date,
        'end_date': subscription.end_date,
        'unlimited': subscription.unlimited,
    }

    return render(request, 'customer/subscriptions/update.html', context)


@login_required
def custumer_subscriptions_detele(request, custumer_id, sub_id):
    custumer = get_object_or_404(Custumer, id=custumer_id)
    subscription = get_object_or_404(CustumerSubscription, id=sub_id)
    subscription.delete()
    return redirect('custumer_subscriptions', pk=custumer.id)