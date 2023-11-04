from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Country, Language, Local_contact, Representative
from .forms import ClientForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt

def client_list(request):
    clients = Client.objects.all()[:10]
    countries = Country.objects.all()
    context =  {'clients': clients,'countries':countries}
    return render(request, 'client_list.html',context)

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    countries = Country.objects.all()
    page_name = 'update-client'
    context = {'client':client,'countries':countries,'page':page_name}
    return render(request, 'client.html', context)

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Client has been added successfully'})
        
        for err in form.errors:
            print(err)
        return JsonResponse({'message':'An error occured ! please retry again'})
    page_name = 'add-client'
    nbr_clients = Client.objects.all().count()
    client_nbr  = "C{0}".format(nbr_clients + 1)
    countries = Country.objects.all()
    languages = Language.objects.all()
    representatives = Representative.objects.all()
    context = {'client_nbr':client_nbr,
               'countries':countries,
               'languages':languages,
               'representatives':representatives,
               'page':page_name}
    return render(request, 'client.html', context)

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Client has been modified successfully'})
        
        for err in form.errors:
            print(err)
        return JsonResponse({'message':'An error occured ! please retry again'})
    
    countries = Country.objects.all()
    page_name = 'update-client'
    representatives = Representative.objects.all()
    languages = Language.objects.all()
    context = {'client':client,
               'countries':countries,
               'representatives':representatives,
               'languages':languages,
               'page':page_name}
    return render(request, 'client.html', context)

def client_delete(request, pk):
    if request.method == "POST":
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        messages.success(request, 'project has been deleted successfully')
        return redirect('client-list')


