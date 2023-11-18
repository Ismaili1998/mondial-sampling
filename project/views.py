from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, ArticleForm, CommercialOfferForm, Supplier_contactForm, SupplierCommandForm, Confirmed_commercialOfferForm, InvoiceForm, PackingForm
from .models import Project, Supplier, Article, QuoteRequest,ArticleUnit,\
File, CommercialOffer, TimeUnit, Destination, Local_contact, Client_contact,\
Order, SupplierCommand, Invoice, Packing
from .tasks import create_payment_alert
from client.models import Client, Country, Language, Transport, Payment, Currency, Shipping
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from django.http import Http404
from . import translations
from django.contrib.auth.decorators import login_required
import re

@login_required(login_url='sign-in')
def project_home(request):
    clients = Client.objects.all()
    latest_project = Project.objects.order_by('-id').first()
    last_id = latest_project.id if latest_project else 0 
    project_nbr  = "A{0}".format(last_id + 1)
    local_contacts = Local_contact.objects.all()
    client_contacts = Client_contact.objects.all()
    context = {'clients':clients,
               'page':'add-project',
               'local_contacts': local_contacts,
               'client_contacts': client_contacts,
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr=project_nbr)
    clients = Client.objects.all()
    articles = project.article_set.all()[:50]
    page_name = 'update-project'
    local_contacts = Local_contact.objects.all()
    client_contacts = Client_contact.objects.all()
    context = {'project':project,
               'clients':clients, 
               'local_contacts':local_contacts,
               'client_contacts': client_contacts,
               'page':page_name,
               'articles':articles}
    return render(request, 'project_home.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been created successfully')
            return project_detail(request,project.project_nbr)
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
            messages.success(request, 'Project has been updated successfully')
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

def add_article_to_commercialOffer(request, offer_pk, article_nbr):
    try:
        commercialOffer = get_object_or_404(CommercialOffer, id=offer_pk)
        article = get_object_or_404(Article, article_nbr=article_nbr)
        order = Order(article=article, quantity=0, margin=0, commercialOffer=commercialOffer)
        order.save()
    except Article.DoesNotExist or CommercialOffer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article or offer not found'})
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
               'orders':commercialOffer.order_set.all()}
    return render(request, 'commercialOffer_edit.html',context) 

    
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


def commercialOffer_detail(commercialOffer):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    return {'commercialOffer':commercialOffer,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings,
               'orders':commercialOffer.order_set.all()}


def quoteRequest_detail(quoteRequest):
   return  {'quoteRequest':quoteRequest, 
            'orders':quoteRequest.order_set.all()}

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    commercialOffer = order.commercialOffer
    quoteRequest = order.quoteRequest
    order.delete()
    if commercialOffer:
        return render(request, 'commercialOffer_edit.html',commercialOffer_detail(commercialOffer))
    return render(request, 'quoteRequest_edit.html', quoteRequest_detail(quoteRequest))

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
    context = {'countries':countries,
               'page':page_name,
               'languages':languages}
    return render(request, 'supplier.html',context)

def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST, instance=supplier)
        if supplier_form.is_valid():
            supplier = supplier_form.save()
            try:
                supplier_contact_form = Supplier_contactForm(prefix='supplier_contact',
                                                            data=request.POST, 
                                                            instance=supplier.supplier_contact)
                if supplier_contact_form.is_valid():
                    supplier_contact = supplier_contact_form.save(commit=False)
                    supplier_contact.supplier = supplier 
                    supplier_contact.save()
                else:
                    for field, errors in supplier_contact_form.errors.items():
                        for error in errors:
                            print(f"++Field: {field} - Error: {error}")
            except:
                pass
                supplier_contact_form = Supplier_contactForm(prefix='supplier_contact',
                                                            data=request.POST)
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
    page_name = 'update-supplier'
    languages = Language.objects.all()
    context = {'countries':countries,
               'page':page_name,
               'supplier':supplier,
               'languages':languages}
    return render(request, 'supplier.html',context)
        
def get_suppliersByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    # Perform the search query using the keyword
    suppliers = Supplier.objects.filter(supplier_name__icontains=keyword)[:5]
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
        client_nbr = project.client.client_nbr 
        articles = request.POST.getlist('article')
        suppliers = request.POST.getlist('supplier')
        quantities = request.POST.getlist('quantity')
        print(articles, quantities, suppliers)
        if not len(articles) or not len(suppliers):
            messages.error(request, 'Please, select at least one article and one supplier  !')
            return redirect('project-detail',project_nbr)
        index = 1
        try:
            for supplier_id in suppliers:
                supplier = Supplier.objects.get(id=supplier_id)
                quoteRequests = project.quoterequest_set.all()
                if len(quoteRequests):
                    last_request = quoteRequests.order_by('-request_nbr').first()
                    request_nbr = last_request.request_nbr
                    pattern = r'N(\d+)-'
                    index = int(re.search(pattern, request_nbr).group(1)) + 1
                request_nbr = "{0}/N{1}-{2}".format(project_nbr,index, client_nbr)      
                quoteRequest = QuoteRequest.objects.create(project = project,
                                                        supplier=supplier,
                                                        request_nbr=request_nbr)
                for article, quantity in zip(articles, quantities):
                    order = Order(article_id=article, quantity=quantity, quoteRequest=quoteRequest)
                    order.save()
            messages.success(request, 'Quote request has been created successfully')
        except:
                messages.error(request, 'An error occured please retry !')
        return redirect('project-detail',project_nbr)
    
    suppliers = Supplier.objects.all()
    context = {'project':project,'suppliers':suppliers}
    return render(request, 'quoteRequest_create.html',context) 

def update_quoteRequest(request,pk):
    quoteRequest = get_object_or_404(QuoteRequest, id=pk)
    if request.method == 'POST':
        project = quoteRequest.project
        order_ids = request.POST.getlist('order')
        quantities = request.POST.getlist('quantity')
        print(order_ids, quantities)
        try:
            for order_id, quantity in zip(order_ids, quantities):
                order = get_object_or_404(Order, id=order_id)
                order.quantity = quantity
                order.save()
            messages.success(request, 'Quote request has been updated successfully')
        except:
                messages.error(request, 'An error occured please retry !')
        return redirect('project-detail',project.project_nbr)
    return render(request, 'quoteRequest_edit.html',context = quoteRequest_detail(quoteRequest)) 



def add_article_to_quoteRequest(request, request_pk, article_nbr):
    quoteRequest = get_object_or_404(QuoteRequest, id=request_pk)
    article = get_object_or_404(Article, article_nbr=article_nbr)
    order = Order(article=article, quoteRequest=quoteRequest)
    order.save()
    return render(request, 'quoteRequest_edit.html',context = quoteRequest_detail(quoteRequest))

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
            offers = project.commercialoffer_set.all()
            index = 1
            if len(offers):
                last_offer = offers.order_by('-offer_nbr').first()
                offer_nbr = last_offer.offer_nbr
                pattern = r'G(\d+)-'
                index = int(re.search(pattern, offer_nbr).group(1)) + 1      
            project_nbr = project.project_nbr
            client_nbr = project.client.client_nbr
            offer_nbr = "{0}/G{1}-{2}".format(project_nbr, index, client_nbr)
            commercialOffer = form.save(commit=False)
            commercialOffer.offer_nbr = offer_nbr
            commercialOffer.confirmation_nbr = offer_nbr.replace('G', 'C')
            commercialOffer.save()

            articles = request.POST.getlist('article')
            quantities = request.POST.getlist('quantity')
            margins = request.POST.getlist('article-margin')
            for article, quantity, margin in zip(articles, quantities, margins):
                order = Order(article_id=article, quantity=quantity, margin=margin, commercialOffer=commercialOffer)
                order.save()
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
               'articles':articles}
    return render(request, 'commercialOffer_create.html',context) 

def update_commercialOffer(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if request.method == 'POST':
        project = commercialOffer.project
        form = CommercialOfferForm(request.POST,instance=commercialOffer)
        if form.is_valid():
            form.save()
            order_ids = request.POST.getlist('order')
            quantities = request.POST.getlist('quantity')
            margins = request.POST.getlist('article-margin')
            for order_id, quantity, margin in zip(order_ids, quantities, margins):
                order = get_object_or_404(Order, id=order_id)
                order.quantity = quantity
                order.margin = margin
                order.save()
            messages.success(request, 'Commercial offer has been updated successfully')
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
               'orders':commercialOffer.order_set.all()}
    return render(request, 'commercialOffer_edit.html',context) 

def delete_commercialOffer(request, pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=pk)
    project = commercialOffer.project 
    if request.method == 'POST':
        commercialOffer.delete()
        messages.success(request, 'commercial offer has been deleted successfully')
    return redirect('project-detail',project.project_nbr)

def print_commercialOffer(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'commercialOffer_print.html', context)


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


def confirm_commercialOffer(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if request.method == 'POST':
        if commercialOffer.confirmed:
            messages.error(request, 'Offer already confirmed !')
            return redirect('project-detail', commercialOffer.project.project_nbr)
        confirmedOffer = Confirmed_commercialOfferForm(request.POST)
        if  confirmedOffer.is_valid():
            commercialOffer.confirmed = True
            commercialOffer.save()
            confirmedOffer = confirmedOffer.save(commit=False)
            confirmedOffer.confirmation_nbr = commercialOffer.offer_nbr.replace('G','C') 
            confirmedOffer.commercialOffer = commercialOffer
            confirmedOffer.save()
            messages.success(request, 'Project has been created successfully')
        else:
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', commercialOffer.project.project_nbr)
    
    context = {"commercialOffer":commercialOffer}
    return render(request, 'confirme_commercialOffer.html', context)

def cancel_confirmedOrder(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if commercialOffer.confirmed:
        commercialOffer.confirmed = False
        confirmedOffer = commercialOffer.confirmed_commercialoffer
        confirmedOffer.delete()
        commercialOffer.save()
    return redirect('project-detail', commercialOffer.project.project_nbr)

def print_confirmOrder(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 
               'translations':filtered_translations}
    return render(request, 'confirmOrder_print.html', context)

def create_invoice(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    if request.method == 'POST':
        invoice = InvoiceForm(request.POST)
        if  invoice.is_valid():
            invoice = invoice.save(commit=False)
            invoice.invoice_nbr = commercialOffer.offer_nbr.replace('G','TN') 
            invoice.commercialOffer = commercialOffer
            invoice.save()
            return redirect('project-detail', commercialOffer.project.project_nbr)
    
    context = {"commercialOffer":commercialOffer}
    return render(request, 'create_invoice.html', context)

def print_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.commercialOffer
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer,
               'invoice':invoice, 
               'translations':filtered_translations}
    return render(request, 'invoice_print.html', context)

def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    project_nbr = invoice.commercialOffer.project.project_nbr
    if request.method == "POST":
        messages.success(request, 'invoice has been deleted successfully !')
        invoice.delete()
    return redirect('project-detail', project_nbr)


def supplierCommand_detail(quoteRequest,page_name):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    currencies = Currency.objects.all()
    return {'quoteRequest':quoteRequest,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'page':page_name,
               'orders':quoteRequest.order_set.all()}


def supplier_command(request, request_pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=request_pk)
    if request.method == 'POST':
        form = SupplierCommandForm(request.POST)
        if form.is_valid():
            supplierCommand = form.save(commit=False)
            supplierCommand.quoteRequest = quoteRequest
            supplierCommand.command_nbr = quoteRequest.request_nbr.replace('N','B')
            supplierCommand.save()
            due_date = supplierCommand.payment_date 
            create_payment_alert.apply_async(args=[due_date], eta=due_date)
            messages.success(request, 'Command has been created successfully.')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', quoteRequest.project.project_nbr)
    return render(request, 'supplier_command.html', context=supplierCommand_detail(quoteRequest,'create-command'))


def update_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    quoteRequest = supplierCommand.quoteRequest
    if request.method == 'POST':
        form = SupplierCommandForm(request.POST, instance=supplierCommand)
        if form.is_valid():
            supplierCommand.save()
            due_date = supplierCommand.payment_date 
            create_payment_alert.delay(120)
            messages.success(request, 'Command has been updated successfully.')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', quoteRequest.project.project_nbr)
    return render(request, 'supplier_command.html', context=supplierCommand_detail(quoteRequest,'update-command'))

def print_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    quoteRequest = supplierCommand.quoteRequest
    language_code = 'fr'
    try:
        language_code = quoteRequest.supplier.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'quoteRequest':quoteRequest, 
               'translations':filtered_translations}
    return render(request, 'supplierCommand_print.html', context)

from django.db.models import  Sum, F, ExpressionWrapper, FloatField
def calculate_totals_by_hsCode(orders_queryset):
    orders_by_hsCode = {}
    for order in orders_queryset:
        hs_code = order.article.hs_code  # Assuming there is an attribute 'hs_code' in your order object
    
        if hs_code not in orders_by_hsCode:
            orders_by_hsCode[hs_code] = {"total_quantities": 0, "total_price": 0}

        orders_by_hsCode[hs_code]["total_quantities"] += order.quantity
        orders_by_hsCode[hs_code]["total_price"] += order.get_selling_price()
    return orders_by_hsCode


def print_customsReport(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.commercialOffer 
    orders = commercialOffer.order_set.all()
    orders_by_hsCode = calculate_totals_by_hsCode(orders)
    language_code = 'fr'
    try:
        language_code = commercialOffer.supplier.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {"commercialOffer":commercialOffer,
               "invoice":invoice, 
               "orders_by_hsCode":orders_by_hsCode.items(),
               "translations":filtered_translations, }
    return render(request,'customs_report.html', context)



def create_packing(request,invoice_pk):
    invoice = get_object_or_404(Invoice, id=invoice_pk)
    if request.method == 'POST':
        form = PackingForm(request.POST)
        if form.is_valid():
            packing = form.save(commit=False)
            packing.invoice = invoice
            packing.save()
            return redirect('project-detail', invoice.commercialOffer.project.project_nbr)
    context = {"invoice":invoice, "form_name":"create"}
    return render(request,'create_packing.html', context)

def update_packing(request, pk):
    packing = get_object_or_404(Packing, id=pk)
    invoice = packing.invoice
    if request.method == 'POST':
        form = PackingForm(request.POST, instance=packing)
        if form.is_valid():
            packing.save()
            return redirect('project-detail', invoice.commercialOffer.project.project_nbr)
    
    context = {"invoice":invoice, 
                "packing":packing, 
                "form_name":"update"}
    return render(request,'create_packing.html', context)
        
def print_packing(request, pk):
    packing = get_object_or_404(Packing, id=pk)
    invoice = packing.invoice
    commercialOffer = invoice.commercialOffer
    language_code = 'fr'
    try:
        language_code = commercialOffer.supplier.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {"commercialOffer":commercialOffer,
            "packing":packing,
            "invoice":invoice, 
            "translations":filtered_translations, }
    return render(request,'packing_print.html', context)



def print_tag(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.commercialOffer
    language_code = 'fr'
    try:
        language_code = commercialOffer.supplier.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {"commercialOffer":commercialOffer,
            "invoice":invoice, 
            "translations":filtered_translations, }
    return render(request,'tag_print.html', context)