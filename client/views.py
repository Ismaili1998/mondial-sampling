from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Country, Language, Transport, Payment
from .forms import ClientForm

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
            messages.success(request, 'Client has been created successfully')
        else:
            messages.error(request, 'An error occured ! please retry again')
            for err in form.errors:
                print(err)
        return redirect('project-home')
    
    page_name = 'add-client'
    countries = Country.objects.all()
    languages = Language.objects.all()
    nbr_clients = Client.objects.all().count()
    client_nbr  = "C{0}".format(nbr_clients + 1)
    context = {'page':page_name,
               'countries':countries,
               'client_nbr':client_nbr,
               'languages':languages}
    return render(request,'client.html',context)

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client has been modified successfully')
        else:
            messages.error(request, 'An error occured ! please retry again ')
            for err in form.errors:
                print(err)
        return redirect('project-home')
    countries = Country.objects.all()
    page_name = 'update-client'
    languages = Language.objects.all()
    context = {'client':client,
               'countries':countries,
               'languages':languages,
               'page':page_name}
    return render(request, 'client.html', context)

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    messages.success(request, 'project has been deleted successfully')
    return redirect('client-list')


