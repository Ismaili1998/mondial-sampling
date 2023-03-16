from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm
from .models import Project
from client.models import Client
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

def project_home(request):
    clients =Client.objects.all()
    context = {'clients':clients}
    return render(request, 'project_home.html',context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_home.html', {'project': project})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been created successfully')
        else:
            messages.error(request, 'An error occured, please retry')

    return redirect('project-home')

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been modified successfully')
            return redirect('project_home', pk=project.pk)
        else:
            messages.error(request, 'An error occured !, please retry')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_home.html', {'form': form})

def project_delete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request, 'project has been deleted successfully')
    return redirect('project_home')

@csrf_exempt
def get_projectsByKeyWord(request):
    data = {}
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if len(keyword):
            projects = Project.objects.filter(project_nbr__icontains=keyword).values('project_nbr')
            data = list(projects)          
    return JsonResponse(data, safe=False)