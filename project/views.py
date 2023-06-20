from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, ArticleForm, CommercialOfferForm
from .models import Project, Supplier, Article, QuoteRequest,ArticleUnit, File, CommercialOffer, TimeUnit, Destination
from client.models import Client, Country, Language, Transport, Payment, Currency, Shipping
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from django.http import Http404
from . import translations


def project_home(request):
    clients = Client.objects.all()
    latest_project = Project.objects.order_by('-id').first()
    last_id = latest_project.id if latest_project else 0 
    project_nbr  = "P{0}".format(last_id + 1)
    context = {'clients':clients,
               'page':'add-project',
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr=project_nbr)
    clients = Client.objects.all()
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
                                       description="")
            project_file.save()
            filenames.append(project_file.file.name)
        return JsonResponse({'message': 'files have been added successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'})

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
            form.save()
            return JsonResponse({'message': 'Article has been modified successfully'})
        else:
            for err in form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
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
            return JsonResponse({'message': 'Article has been modified successfully'})
        else:
            messages.error(request, 'An error occured ! please retry again ')
            for err in form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
    
    page_name = 'update-article'
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    article_units = ArticleUnit.objects.all()
    context = {'article':article, 
               'projects':projects, 
               'suppliers':suppliers,
               'article_units':article_units,
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
            return redirect('project-detail', project_nbr)
        except:
            return JsonResponse({'message':'An error occured ! please retry again'})

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
        request_id = (last_quotRequest.id if last_quotRequest else 0 ) + 1
        try:
            for index,supplier_id in enumerate(suppliers,1):
                supplier = Supplier.objects.get(id=supplier_id)
                last_quotRequest = QuoteRequest.objects.order_by('id').last()
                request_nbr = "R{0}/{1}-N{2}-{3}".format(request_id,
                                                    project_nbr,
                                                    index,
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
    language_code = quoteRequest.supplier.language.language_code 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'quoteRequest':quoteRequest,'translations':filtered_translations}
    return render(request, 'quoteRequest_pdf.html', context)


#======================= Commercial offer area ====================================#
def create_commercialOffer(request,project_pk):
    project = get_object_or_404(Project, id=project_pk)
    project_nbr = project.project_nbr
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST)
        if form.is_valid():
            commercialOffer = form.save()
            last_commercialOffer = CommercialOffer.objects.order_by('id').last()
            offer_id = last_commercialOffer.id if last_commercialOffer else 0
            offer_id += 1
            offer_nbr = "{0}/G-{1}-{2}".format(project_nbr,
                                                offer_id,
                                                project.client.client_nbr)
            commercialOffer.offer_nbr = offer_nbr
            commercialOffer.save()
            messages.success(request, 'Commercial offer has been created successfully')
            return redirect('project-detail', project_nbr)
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
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    context = {'project':project,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings':shippings,
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
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    context = {'commercialOffer':commercialOffer,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings,
               'page':'update-commercialOffer',
               'articles':commercialOffer.articles.all()}
    return render(request, 'commercialOffer.html',context) 

def create_commercialOffer_pdfReport(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = commercialOffer.project.client.language.language_code 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'commercialOffer_pdf.html', context)


def print_technicalOffer(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = commercialOffer.project.client.language.language_code 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'technicalOffer_print.html', context)

