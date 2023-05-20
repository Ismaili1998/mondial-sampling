from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, ArticleForm, CommercialOfferForm
from .models import Project, Supplier, Article, QuoteRequest,ArticleUnit, File, CommercialOffer, TimeUnit, Payment, Transport, Destination
from client.models import Client, Country, Language
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
from django.conf import settings
from django.views.static import serve
from django.http import Http404


def project_home(request):
    clients = Client.objects.all()
    nbr_projects = Project.objects.all().count()
    project_nbr  = "P{0}".format(nbr_projects + 1)
    context = {'clients':clients,
               'page':'add-project',
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr=project_nbr)
    clients =Client.objects.all()
    articles = project.articles.all()
    page_name = 'update-project'
    context = {'project':project,
               'clients':clients, 
               'page':page_name,
               'articles':articles}
    return render(request, 'project_home.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project has been created successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
    return redirect('project-home')

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been modified successfully')
        else:
            messages.error(request, 'An error occured, please retry')

    return redirect('project-detail', project.project_nbr)


def project_delete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request, 'project has been deleted successfully')
    return redirect('project_home')

@csrf_exempt
def get_projectsByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    projects = Project.objects.filter(project_nbr__icontains=keyword).values_list('project_nbr', flat=True)
    return JsonResponse(list(projects), safe=False)

@csrf_exempt
def upload_file_to_project(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('files')
        filenames = []
        for file in files:
            project_file = File(project=project,
                                       file=file,
                                       description="ici")
            project_file.save()
            filenames.append(project_file.file.name)
        return JsonResponse({'filenames': filenames})
    else:
        return JsonResponse({'error': 'Invalid request'})

def download_file(request, file_pk):
    try:
        project_file = File.objects.get(id=file_pk)
    except File.DoesNotExist:
        raise Http404
    # Use Django's built-in `serve()` view to return the file
    return serve(request, project_file.file.name, document_root=settings.MEDIA_ROOT)
#======================= Article area ====================================#
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, 'Article has been created successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-home')
    
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    article_units = ArticleUnit.objects.all()
    article_nbr = Article.objects.all().count()
    article_nbr = "A{0}".format(article_nbr)
    page_name = 'add-article'
    context = {'projects':projects, 
               'suppliers':suppliers,
               'article_units':article_units,
               'article_nbr':article_nbr,
               'page':page_name}
    return render(request, 'article.html',context)

def article_detail(request, article_nbr):
    article= get_object_or_404(Article, article_nbr = article_nbr)
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    context = {'article':article, 'projects':projects, 'suppliers':suppliers}
    return render(request, 'article.html', context)

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article has been modified successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-home')
    
    page_name = 'update-article'
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    units = ArticleUnit.objects.all()
    context = {'article':article, 
               'projects':projects, 
               'suppliers':suppliers,
               'units':units,
               'page':page_name}
    return render(request, 'article.html', context)

@csrf_exempt
def get_articlesByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    articles = Article.objects.filter(article_nbr__icontains=keyword).values_list('article_nbr', flat=True)
    return JsonResponse(list(articles), safe=False)

def add_article_to_project(request):
    if request.method == 'POST':
        project_nbr = request.POST['project_nbr']
        article_nbr = request.POST['article_nbr']
        try:
            article = Article.objects.get(article_nbr=article_nbr)
            project = Project.objects.get(project_nbr=project_nbr)
            project.articles.add(article)
            project.save()
        except Article.DoesNotExist:
            pass
        return redirect('project-detail', project.project_nbr)
    return redirect('project-home')

def article_delete(request, pk):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        messages.success(request, 'Article has been deleted successfully')
    return redirect('project-home')

#======================= supplier area ====================================#
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier has been created successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        
        return redirect('project-home')
    countries = Country.objects.all()
    page_name = 'add-supplier'
    languages = Language.objects.all()
    context = {'countries':countries,'page':page_name,'languages':languages}
    return render(request, 'supplier.html',context)

def search_supplier(request):
    if request.method == 'GET':
        # Get the keyword from the request
        keyword = request.GET.get('keyword', '')  
        # Search for suppliers with name containing the keyword
        suppliers = Supplier.objects.filter(name__icontains=keyword)  
        return render(request, 'supplier/search.html', {'suppliers': suppliers, 'keyword': keyword})


#======================= quoteRequest area ====================================#
def create_quoteRequest(request,project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        project_nbr = project.project_nbr
        articles = request.POST.getlist('articles')
        suppliers = request.POST.getlist('suppliers')
        last_quotRequest = QuoteRequest.objects.order_by('id').last()
        if last_quotRequest:
            request_id = last_quotRequest.id + 1
        else:
            request_id = 1
        try:
            for index,supplier_id in enumerate(suppliers,1):
                supplier = Supplier.objects.get(id=supplier_id)
                # if not QuoteRequest.objects.filter(project=project, 
                #                                 supplier=supplier, 
                #                                 articles__in=articles).exists():
                last_quotRequest = QuoteRequest.objects.order_by('id').last()
                request_nbr = "R{0}/{1}-N{2}-{3}{4}".format(request_id,
                                                    project_nbr,
                                                    index,
                                                    project.client.country.abbreviation,
                                                    project.client.client_nbr)
                quoteRequest = QuoteRequest.objects.create(project = project,
                                                        supplier=supplier,
                                                        request_nbr=request_nbr)
                quoteRequest.articles.set(articles)
                request_id+=1
            messages.success(request, 'Quote request has been created successfully')
        except:
                messages.error(request, 'An error occured please retry !')

        return redirect('project-detail',project_nbr)
    
    suppliers = Supplier.objects.all()
    context = {'project':project,'suppliers':suppliers}
    return render(request, 'quoteRequest.html',context) 

def create_quoteRequest_pdfReport(request, request_pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=request_pk)
    context = {'quoteRequest':quoteRequest}
    return render(request, 'quoteRequest_pdf.html', context)


#======================= Commercial offer area ====================================#
def create_commercialOffer(request,project_pk):
    project = get_object_or_404(Project, id=project_pk)
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Commercial offer has been created successfully')
            return redirect('project-detail', project.project_nbr)
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    # Print or log the error details
                    print(f"Field: {field}, Error: {error.message}")
            messages.error(request, 'An error occured, please retry')
            return redirect('project-detail', project.project_nbr)
        
    article_ids = request.GET.getlist('articles[]')
    try:
        articles = Article.objects.filter(id__in=article_ids)
    except Article.DoesNotExist:
            messages.error(request, 'An error occured, please retry') 
            return redirect('project-detail', project.project_nbr) 

    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    context = {'project':project,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'page':'add-commercialOffer',
               'articles':articles}
    return render(request, 'commercialOffer.html',context) 

def update_commercialOffer(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if request.method == 'POST':
        project = commercialOffer.project
        form = CommercialOfferForm(request.POST,instance=commercialOffer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Commercial offer has been created successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', project.project_nbr)
    
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    context = {'commercialOffer':commercialOffer,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'page':'update-commercialOffer',
               'articles':commercialOffer.articles.all()}
    return render(request, 'commercialOffer.html',context) 

def create_commercialOffer_pdfReport(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    context = {'commercialOffer':commercialOffer}
    return render(request, 'commercialOffer_pdf.html', context)

