from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, ArticleForm, CommercialOfferForm, Supplier_contactForm
from .models import Project, Supplier, Article, QuoteRequest,ArticleUnit, File, CommercialOffer, TimeUnit, Destination, Local_contact, Client_contact, Buyer
from client.models import Client, Country, Language, Transport, Payment, Currency, Shipping
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from django.http import Http404
from . import translations
from django.contrib.auth.decorators import login_required
from .forms import Client_contactForm, BuyerForm

@login_required(login_url='sign-in')
def project_home(request):
    clients = Client.objects.all()
    latest_project = Project.objects.order_by('-id').first()
    last_id = latest_project.id if latest_project else 0 
    project_nbr  = "P{0}".format(last_id + 1)
    local_contacts = Local_contact.objects.all()
    context = {'clients':clients,
               'page':'add-project',
               'local_contacts': local_contacts,
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr=project_nbr)
    clients = Client.objects.all()
    articles = project.article_set.all()[:50]
    page_name = 'update-project'
    local_contacts = Local_contact.objects.all()
    context = {'project':project,
               'clients':clients, 
               'local_contacts':local_contacts,
               'page':page_name,
               'articles':articles}
    return render(request, 'project_home.html', context)

def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            client_contact_form = Client_contactForm(prefix='client_contact', data=request.POST)
            if client_contact_form.is_valid():
                client_contact = client_contact_form.save()
                project.client_contact = client_contact 
            else:
                for field, errors in client_contact_form.errors.items():
                    for error in errors:
                        print(f"Field: {field} - Error: {error}")
            project.save()
            buyer_form = BuyerForm(prefix='buyer', data=request.POST)
            if buyer_form.is_valid():
                buyer = buyer_form.save(commit=False)
                buyer.project = project 
                buyer.save()
            else:
                for err in buyer_form.errors:
                    print(err) 
            messages.success(request, 'Project has been created successfully')
            return project_detail(request,project.project_nbr)
        else:
            for err in project_form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
    return redirect('project-home')

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            client_contact_form = Client_contactForm(prefix='client_contact',data=request.POST)
            if client_contact_form.is_valid():
                name =  client_contact_form.cleaned_data['name']
                email =  client_contact_form.cleaned_data['email']
                phone_number =  client_contact_form.cleaned_data['phone_number']
                client_contact, created = Client_contact.objects.get_or_create(name=name)
                client_contact.email = email
                client_contact.phone_number = phone_number
                client_contact.save()
                project.client_contact = client_contact
            project.save()
            try:
                buyer_form = BuyerForm(prefix='buyer',data=request.POST,instance=project.buyer)
                if buyer_form.is_valid():
                    buyer_form.save()
            except:
                buyer_form = BuyerForm(prefix='buyer',data=request.POST)
                if buyer_form.is_valid():
                    buyer = buyer_form.save(commit=False)
                    buyer.project = project
                    buyer.save()
            messages.success(request, 'Project has been created successfully')
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
    projects = Project.objects.filter(project_nbr__icontains=keyword).values_list('project_nbr', flat=True)[:20]
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
    articles = Article.objects.filter(article_nbr__icontains=keyword).values_list('article_nbr', flat=True)[:10]
    return JsonResponse(list(articles), safe=False)

def add_article_to_project(request):
    if request.method == 'POST':
        project_nbr = request.POST['project_nbr']
        article_nbr = request.POST['article_nbr']
        try:
            project = Project.objects.get(project_nbr=project_nbr)
            article = Article.objects.get(article_nbr=article_nbr)
            article.project = project
            article.save()
            messages.success(request,'Article has been added to project succesfully')
        except:
            messages.error(request,'An error occured ! please retry again')
        return redirect('project-detail', project_nbr)

def remove_article_from_project(request, article_pk):
    article = Article.objects.get(id=article_pk)
    project = article.project 
    article.project = None
    article.save()
    messages.success(request,'Article has been removed from project succesfully')
    return redirect('project-detail', project.project_nbr)

#======================= supplier area ====================================#
def supplier_create(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier = supplier_form.save()
            supplier_contact_form =Supplier_contactForm(prefix='supplier_contact', data=request.POST)
            if supplier_contact_form.is_valid():
                supplier_contact = supplier_contact_form.save(commit=False)
                supplier_contact.supplier = supplier 
                supplier_contact.save()
            else:
                for field, errors in supplier_contact_form.errors.items():
                    for error in errors:
                        print(f"Field: {field} - Error: {error}")
            return JsonResponse({'message': 'Client has been added successfully'})
        else:
            for err in supplier_form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
    
    countries = Country.objects.all()
    page_name = 'add-supplier'
    languages = Language.objects.all()
    local_contacts = Local_contact.objects.all()
    context = {'countries':countries,
               'page':page_name,
               'languages':languages,
               'local_contacts':local_contacts}
    return render(request, 'supplier.html',context)


def get_suppliersByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    # Perform the search query using the keyword
    suppliers = Supplier.objects.filter(supplier_name__icontains=keyword)[:10]
    # Prepare the suppliers' data for JSON serialization
    supplier_data = []
    if len(suppliers):
        for supplier in suppliers:
            supplier_data.append({
                'id': supplier.id,
                'supplier_name': supplier.supplier_name or '',
                'supplier_nbr':supplier.supplier_nbr,
                'country': ''
            })

    # Return the suppliers' data as JSON response
    return JsonResponse({'suppliers': supplier_data})



#======================= quoteRequest area ====================================#
def create_quoteRequest(request,project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        project_nbr = project.project_nbr
        articles = request.POST.getlist('articles')
        suppliers = request.POST.getlist('suppliers')
        if not len(articles) or not len(suppliers):
            messages.error(request, 'Please, select at least one article and one supplier  !')
            return redirect('project-detail',project_nbr)
        try:
            index = project.quoterequest_set.all().count() + 1
            for supplier_id in suppliers:
                supplier = Supplier.objects.get(id=supplier_id)
                request_nbr = "{0}/N{1}-{2}".format(project_nbr,
                                                index,
                                                project.client.client_nbr)
                quoteRequest = QuoteRequest.objects.create(project = project,
                                                        supplier=supplier,
                                                        request_nbr=request_nbr)
                quoteRequest.articles.set(articles)
                index+=1
            messages.success(request, 'Quote request has been created successfully')
        except:
                messages.error(request, 'An error occured please retry !')

        return redirect('project-detail',project_nbr)
    
    suppliers = Supplier.objects.all()
    context = {'project':project,'suppliers':suppliers}
    return render(request, 'quoteRequest.html',context) 

def create_quoteRequest_pdfReport(request, request_pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=request_pk)
    language_code = 'fr'
    try:
        language_code = quoteRequest.supplier.language.language_code
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'quoteRequest':quoteRequest,'translations':filtered_translations}
    return render(request, 'quoteRequest_pdf.html', context)


def delete_quoteRequest(request, pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=pk)
    project = quoteRequest.project 
    if request.method == 'POST':
        quoteRequest.delete()
        messages.success(request, 'quoteRequest has been deleted successfully')
    return redirect('project-detail',project.project_nbr)
#======================= Commercial offer area ====================================#
def create_commercialOffer(request,project_pk):
    project = get_object_or_404(Project, id=project_pk)
    project_nbr = project.project_nbr
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST)
        if form.is_valid():
            commercialOffer = form.save()
            index = project.commercialoffer_set.all().count()
            offer_nbr = "{0}/G{1}-{2}".format(project_nbr,
                                                index,
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

def delete_commercialOffer(request, pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=pk)
    project = commercialOffer.project 
    if request.method == 'POST':
        commercialOffer.delete()
        messages.success(request, 'commercial offer has been deleted successfully')
    return redirect('project-detail',project.project_nbr)

def create_commercialOffer_pdfReport(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'commercialOffer_pdf.html', context)


def print_technicalOffer(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'technicalOffer_print.html', context)

