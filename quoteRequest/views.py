from django.shortcuts import render, redirect, get_object_or_404
from project.models import Project, TimeUnit, Currency, Payment, Supplier
from .models import QuoteRequest, SupplierCommand
from .forms import SupplierCommandForm
from project import translations
from django.contrib import messages
from order.models  import Article, Order 
import re

def quoteRequest_detail(quoteRequest):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    currencies = Currency.objects.all()
    return  {'quoteRequest':quoteRequest,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments, 
               'orders':quoteRequest.order_set.all()}


def supplierCommand_detail(supplierCommand):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    currencies = Currency.objects.all()
    return {'supplierCommand':supplierCommand,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'orders':supplierCommand.order_set.all()}


def get_rank(quotes) -> int:
    rank = 1
    if len(quotes):
        last_quote = quotes.order_by('-rank').first()
        rank = last_quote.rank + 1
    return rank 

def create_quoteRequest(request,project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        project_nbr = project.project_nbr
        client_nbr = project.client.client_nbr 
        articles = request.POST.getlist('article')
        suppliers = request.POST.getlist('supplier')
        quantities = request.POST.getlist('quantity')
        if not len(articles) or not len(suppliers):
            messages.error(request, 'An error occured, please retry !')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        try:
            for supplier_id in suppliers:
                supplier = Supplier.objects.get(id=supplier_id)
                quoteRequests = project.quoterequest_set.all()
                rank = get_rank(quoteRequests) 
                request_nbr = "{0}/N{1}-{2}".format(project_nbr, rank, client_nbr)
                quoteRequest = QuoteRequest.objects.create(project = project,
                                                        supplier=supplier,
                                                        rank=rank,
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
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    suppliers = Supplier.objects.all()
    context = {'project':project,'suppliers':suppliers}
    return render(request, 'quoteRequest_create.html',context) 


def update_orders(order_ids, quantities, purchase_prices):
    for order_id, quantity, purchase_price in zip(order_ids, quantities, purchase_prices):
                order = get_object_or_404(Order, id=order_id)
                order.quantity = quantity
                order.purchase_price = purchase_price
                order.save()

def update_quoteRequest(request,pk):
    quoteRequest = get_object_or_404(QuoteRequest, id=pk)
    if request.method == 'POST':
        order_ids = request.POST.getlist('order')
        quantities = request.POST.getlist('quantity')
        purchase_prices = request.POST.getlist('purchase-price')
        try:
            update_orders(order_ids, quantities, purchase_prices)
            messages.success(request, 'Quote request has been updated successfully')
        except:
                messages.error(request, 'An error occured please retry !')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'quoteRequest_edit.html',context = quoteRequest_detail(quoteRequest))
 
def print_quoteRequest(request, request_pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=request_pk)
    try:
        language_code = quoteRequest.supplier.language.language_code
    except:
        language_code = 'fr'
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = quoteRequest_detail(quoteRequest)
    context['translations'] = filtered_translations
    return render(request, 'quoteRequest_print.html', context)


def add_article_to_quoteRequest(request, request_pk, article_nbr):
    quoteRequest = get_object_or_404(QuoteRequest, id=request_pk)
    article = get_object_or_404(Article, article_nbr=article_nbr)
    order = Order(article=article, quoteRequest=quoteRequest)
    order.save()
    return render(request, 'quoteRequest_edit.html',context = quoteRequest_detail(quoteRequest))

def add_article_to_supplierCommand(request, request_pk, article_nbr):
    supplierCommand = get_object_or_404(SupplierCommand, id=request_pk)
    article = get_object_or_404(Article, article_nbr=article_nbr)
    order = Order(article=article, confirmed_quoteRequest=supplierCommand)
    order.save()
    return render(request, 'supplierCommand_edit.html',context = supplierCommand_detail(supplierCommand))

def delete_quoteRequest(request, pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=pk)
    project = quoteRequest.project 
    if request.method == 'POST':
        quoteRequest.delete()
        messages.success(request, 'quoteRequest has been deleted successfully')
    return redirect('project-detail',project.project_nbr)


def create_supplierCommand(request, request_pk):
    quoteRequest = get_object_or_404(QuoteRequest, pk=request_pk)
    project = quoteRequest.project
    project_nbr = project.project_nbr 
    if request.method == 'POST':
        form = SupplierCommandForm(request.POST)
        if form.is_valid():
            supplierCommand = form.save(commit=False)
            supplierCommand.project = quoteRequest.project
            supplierCommand.supplier = quoteRequest.supplier
            client_nbr = project.client.client_nbr
            rank = get_rank(project.suppliercommand_set.all())
            supplierCommand.command_nbr =  "{0}/B{1}-{2}".format(project_nbr, rank, client_nbr)
            supplierCommand.rank = rank
            supplierCommand.save()
            orders = quoteRequest.order_set.all()
            for order in orders:
                order.quoteRequest = order.id = None 
                order.confirmed_quoteRequest = supplierCommand
                order.save()
            messages.success(request, 'Command has been created successfully.')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'supplierCommand_create.html', context=quoteRequest_detail(quoteRequest))

def update_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    if request.method == 'POST':
        form = SupplierCommandForm(request.POST, instance=supplierCommand)
        if form.is_valid():
            form.save()
        else:
            for err in form.errors:
                print(err)
        order_ids = request.POST.getlist('order')
        quantities = request.POST.getlist('quantity')
        purchase_prices = request.POST.getlist('purchase-price')
        try:
            update_orders(order_ids, quantities, purchase_prices)
            messages.success(request, 'Supplier command has been updated successfully')
        except:
            messages.error(request, 'Failed to save orders update !')        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'supplierCommand_edit.html', context = supplierCommand_detail(supplierCommand))

def print_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    try:
        language_code = supplierCommand.supplier.language.language_code 
    except:
        language_code = 'fr' 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = supplierCommand_detail(supplierCommand)
    context['translations'] = filtered_translations
    return render(request, 'supplierCommand_print.html', context)


def delete_order_from_quoteRequest(request, pk):
    order = get_object_or_404(Order, pk=pk)
    quoteRequest = order.quoteRequest
    order.delete()
    return render(request, 'quoteRequest_edit.html', context = quoteRequest_detail(quoteRequest))


def delete_order_from_supplierCommand(request, pk):
    order = get_object_or_404(Order, pk=pk)
    supplierCommand = order.confirmed_quoteRequest
    order.delete()
    return render(request, 'supplierCommand_edit.html', context = supplierCommand_detail(supplierCommand))

def delete_supplierCommand(request, pk):
    supplierCommand = get_object_or_404(SupplierCommand, id=pk)
    project_nbr = supplierCommand.project.project_nbr
    if request.method == "POST":
        supplierCommand.delete()
        messages.success(request, 'Supplier command has been deleted successfully !')
    return redirect('project-detail', project_nbr)