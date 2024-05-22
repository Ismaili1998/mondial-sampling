from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Article, ArticleUnit
from .forms import ArticleForm
from django.views.decorators.csrf import csrf_exempt

def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Article has been modified successfully'})
        else:
            for err in form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
    article_units = ArticleUnit.objects.all()
    try:
        last_article = Article.objects.latest('id')
        article_nbr = last_article.id + 1 
    except Article.DoesNotExist:
        article_nbr = 1
    article_nbr = "A{0}".format(article_nbr)
    page_name = 'add-article'
    context = {'article_units':article_units,
               'article_nbr':article_nbr,
               'page':page_name}
    return render(request, 'article.html',context)
   
def article_detail(request, article_nbr):
    article= get_object_or_404(Article, article_nbr = article_nbr)
    context = {'article':article}
    return render(request, 'article.html', context)

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Article has been modified successfully'})
        else:
            for err in form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
    
    page_name = 'update-article'
    article_units = ArticleUnit.objects.all()
    context = {'article':article, 
               'article_units':article_units,
               'page':page_name}
    return render(request, 'article.html', context)

@csrf_exempt
def get_articlesByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    articles = Article.objects.filter(article_nbr__icontains=keyword).values_list('article_nbr', flat=True)[:10]
    return JsonResponse(list(articles), safe=False)


