from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm
from .models import Project
from django.contrib import messages

def project_home(request):
    return render(request, 'project_home.html')

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_home.html', {'project': project})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'project has been created successfully')
            return redirect('project_detail', pk=project.pk)
        else:
            messages.error(request, 'an error occured !, please retry')
    else:
        form = ProjectForm()
    return render(request, 'project_home.html', {'form': form})

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'project has been modified successfully')
            return redirect('project_home', pk=project.pk)
        else:
            messages.error(request, 'an error occured !, please retry')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_home.html', {'form': form})

def project_delete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request, 'project has been deleted successfully')
    return redirect('project_home')
