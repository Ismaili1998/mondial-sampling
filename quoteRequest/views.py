from django.shortcuts import render, redirect, get_object_or_404
from project.models import Project, TimeUnit, Currency, Payment, Supplier
from .models import QuoteRequest, SupplierCommand
from .forms import SupplierCommandForm
from project import translations
from django.contrib import messages
from order.models  import Article, Order 
import re

def quoteRequest_detail(quoteRequest):
   return  {'quoteRequest':quoteRequest, 
            'orders':quoteRequest.order_set.all()}

def create_quoteRequest(request,project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        project_nbr = project.project_nbr
        client_nbr = project.client.client_nbr 
        articles = request.POST.getlist('article')
        suppliers = request.POST.getlist('supplier')
        quantities = request.POST.getlist('quantity')
        if not len(articles) or not len(suppliers):
            messages.error(request, 'Please, select at least one article and one supplier  !')
            return redirect('project-detail',project_nbr)
        index = 1
        try:
            for supplier_id in suppliers:
                supplier = Supplier.objects.get(id=supplier_id)
                quoteRequests = project.quoterequest_set.all()
                if len(quoteRequests):
                    last_request = quoteRequests.order_by('-id').first()
                    request_nbr = last_request.request_nbr
                    pattern = r'N(\d+)-'
                    index = int(re.search(pattern, request_nbr).group(1)) + 1
                request_nbr = "{0}/N{1}-{2}".format(project_nbr,index, client_nbr)
                quoteRequest = QuoteRequest.objects.create(project = project,
                                                        supplier=supplier,
                                                        request_nbr=request_nbr)
                for article_id, quantity in zip(articles, quantities):
                    article = get_object_or_404(Article, id=article_id)
                    order = Order(article=article, quantity=quantity,
                                  purchase_price = article.purchase_price,
                                  quoteRequest=quoteRequest)
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
        purchase_prices = request.POST.getlist('purchase-price')
        try:
            for order_id, quantity, purchase_price in zip(order_ids, quantities, purchase_prices):
                order = get_object_or_404(Order, id=order_id)
                order.quantity = quantity
                order.purchase_price = purchase_price
                order.save()
            messages.success(request, 'Quote request has been updated successfully')
        except:
                messages.error(request, 'An error occured please retry !')
        return redirect('project-detail',project.project_nbr)
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
    return render(request, 'quoteRequest_print.html', context)


def add_article_to_quoteRequest(request, request_pk, article_nbr):
    quoteRequest = get_object_or_404(QuoteRequest, id=request_pk)
    article = get_object_or_404(Article, article_nbr=article_nbr)
    order = Order(article=article, quoteRequest=quoteRequest)
    order.save()
    return render(request, 'quoteRequest_edit.html',context = quoteRequest_detail(quoteRequest))


def delete_quoteRequest(request, pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=pk)
    project = quoteRequest.project 
    if request.method == 'POST':
        quoteRequest.delete()
        messages.success(request, 'quoteRequest has been deleted successfully')
    return redirect('project-detail',project.project_nbr)

def supplierCommand_detail(quoteRequest):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    currencies = Currency.objects.all()
    return {'quoteRequest':quoteRequest,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
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
            messages.success(request, 'Command has been created successfully.')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', quoteRequest.project.project_nbr)
    return render(request, 'supplierCommand_create.html', context=supplierCommand_detail(quoteRequest))

def update_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    quoteRequest = supplierCommand.quoteRequest
    if request.method == 'POST':
        form = SupplierCommandForm(request.POST, instance=supplierCommand)
        if form.is_valid():
            supplierCommand.save()
            messages.success(request, 'Command has been updated successfully.')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', quoteRequest.project.project_nbr)
    return render(request, 'supplierCommand_edit.html', context = supplierCommand_detail(quoteRequest))

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


def delete_order_from_quoteRequest(request, pk):
    order = get_object_or_404(Order, pk=pk)
    quoteRequest = order.quoteRequest
    order.delete()
    return render(request, 'quoteRequest_edit.html', context = quoteRequest_detail(quoteRequest))


def delete_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    project_nbr = supplierCommand.quoteRequest.project.project_nbr
    if request.method == "POST":
        messages.success(request, 'Supplier command has been deleted successfully !')
        supplierCommand.delete()
    return redirect('project-detail', project_nbr)