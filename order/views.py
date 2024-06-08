from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Article, ArticleUnit
from .forms import ArticleForm
from django.views.decorators.csrf import csrf_exempt
from project.views import get_message_error
from project.models import Project
from django.contrib import messages
import os 

def create_article(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            if request.POST.get('project'):
                messages.success(request,'Article has been added to the project succesfully')
                article.projects.add(project)
            else:
                messages.success(request,'Article has been added succesfully')
            return redirect('project-detail', project.id)
        messages.error(request, get_message_error(form))
        return redirect('project-detail', project.id)
    article_units = ArticleUnit.objects.all()
    context = {'article_units':article_units, 'project':project}
    return render(request, 'article.html',context)
   
def article_detail(request, article_nbr):
    article= get_object_or_404(Article, article_nbr = article_nbr)
    context = {'article':article}
    return render(request, 'article.html', context)

def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Article has been modified successfully'})
        return JsonResponse({'error':get_message_error(form)})
    article_units = ArticleUnit.objects.all()
    context = {'article':article, 
               'article_units':article_units}
    return render(request, 'article_edit.html', context)

@csrf_exempt
def get_articlesByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    articles = Article.objects.filter(article_nbr__icontains=keyword).values_list('article_nbr', flat=True)[:10]
    return JsonResponse(list(articles), safe=False)


