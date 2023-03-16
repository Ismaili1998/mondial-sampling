from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Country
from .forms import ClientForm

def client_list(request):
    clients = Client.objects.all()[:10]
    countries = Country.objects.all()
    context =  {'clients': clients,'countries':countries}
    return render(request, 'client_list.html',context)

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    clients = Client.objects.all()[:10]
    countries = Country.objects.all()
    context = {'client':client,'clients':clients,'countries':countries}
    return render(request, 'client_list.html', context)

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client has been created successfully')
        else:
            messages.error(request, 'An error occured ! please retry again ')
    return redirect('client-list')

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, 'project has been modified successfully')
            return redirect('client_detail', pk=client.pk)
        else:
            messages.error(request, 'an error occured !, please retry again ')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_form.html', {'form': form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    messages.success(request, 'project has been deleted successfully')
    return redirect('client-list')


