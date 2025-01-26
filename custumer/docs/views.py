from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from groups_custumer.models import GroupsClass
from custumer.models import Custumer, CustumerDocs


@login_required
def custumer_docs_all(request, pk):
    context = {}
    context['cutumer'] = get_object_or_404(Custumer, id=pk)
    context['docs'] = CustumerDocs.objects.filter(custumer=context['cutumer'])

    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')

        if not name or not file:
            context['error'] = "Название и файл обязательны для заполнения."
            return render(request, 'customer/docs/index.html', context)

        CustumerDocs.objects.create(
                    custumer=context['cutumer'],
                    name=name,
                    files=file,
                )
        return redirect('custumer_docs_all', pk=context['cutumer'].id)

    return render(request, 'customer/docs/index.html', context)



@login_required
def custumer_dos_delet(request, custumer_id, doc_id):
    custumer = get_object_or_404(Custumer, id=custumer_id)
    doc = get_object_or_404(CustumerDocs, id=doc_id)
    doc.delete()
    return redirect('custumer_docs_all', pk=custumer.id)