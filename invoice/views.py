from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InvoiceForm, PackingForm
from .models import Invoice, Packing
from project import translations
from project.models import Bank_info
from commercialOffer.models import Confirmed_commercialOffer
from project.views import get_message_error
from order.models import Order, Article
from project.models import TimeUnit, Destination, \
Currency, Shipping, Transport, Payment
from django.http import JsonResponse
from commercialOffer.views import update_orders

def get_rank(invoices) -> int:
    rank = 1
    if len(invoices):
        last_invoice = invoices.order_by('-rank').first()
        rank = last_invoice.rank + 1
    return rank 

def create_invoice(request, offer_pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, pk=offer_pk)
    project = confirmedOffer.project
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if  form.is_valid():
            invoice = form.save(commit=False)
            invoices = project.invoice_set.all()
            rank = get_rank(invoices)
            invoice.invoice_nbr = "{0}/TN{1}-{2}".format(project.project_nbr, rank, project.client.client_nbr)
            invoice.rank = rank
            invoice.save()
            invoice.clone_orders_from_confirmedOffer(confirmedOffer)
            messages.success(request, 'Invoice has been created successfully !')
        else:
            messages.error(request, get_message_error(form))
        return redirect('project-detail', project.id)
    context = {"confirmedOffer":confirmedOffer}
    return render(request, 'create_invoice.html', context)

def print_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    context = {'invoice':invoice,
               'bank_info':Bank_info.objects.order_by('-id').first(), 
               'translations':get_translation(invoice)}
    return render(request, 'invoice_print.html', context)

def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if request.method == "POST":
        messages.success(request, 'invoice has been deleted successfully !')
        invoice.delete()
    return redirect('project-detail', invoice.project.id)


def calculate_totals_by_hsCode(orders_queryset):
    orders_by_hsCode = {}
    for order in orders_queryset:
        hs_code = order.article.hs_code  
        if hs_code not in orders_by_hsCode:
            orders_by_hsCode[hs_code] = {"total_quantities": 0, "total_price": 0}
        orders_by_hsCode[hs_code]["total_quantities"] += order.quantity
        orders_by_hsCode[hs_code]["total_price"] += order.get_total_selling()
    return orders_by_hsCode

def get_translation(invoice):
    language = invoice.project.client.language
    language_code = language.language_code if language else "fr" 
    return {key:value[language_code] for key, value in translations.translations.items()}

def print_customsReport(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    orders = invoice.order_set.all()
    orders_by_hsCode = calculate_totals_by_hsCode(orders)
    context = {"invoice":invoice, 
               "orders_by_hsCode":orders_by_hsCode.items(),
               "translations":get_translation(invoice)}
    return render(request,'customs_report.html', context)

def create_packing(request,invoice_pk):
    invoice = get_object_or_404(Invoice, id=invoice_pk)
    if request.method == 'POST':
        form = PackingForm(request.POST)
        if form.is_valid():
            packing = form.save(commit=False)
            packing.invoice = invoice
            packing.save()
            messages.success(request,"Packing created successfully")
        else:
            messages.error(request, get_message_error(form))
        return redirect('project-detail', invoice.project.id)
    context = {"invoice":invoice, "form_name":"create"}
    return render(request,'create_packing.html', context)

def update_packing(request, pk):
    packing = get_object_or_404(Packing, id=pk)
    invoice = packing.invoice
    if request.method == 'POST':
        form = PackingForm(request.POST, instance=packing)
        if form.is_valid():
            packing.save()
            messages.success(request,"Packing updated successfully")
        else:
            messages.error(request, get_message_error(form))
        return redirect('project-detail', invoice.project.id)
    context = {"invoice":invoice, 
                "packing":packing, 
                "form_name":"update"}
    return render(request,'create_packing.html', context)


def print_packing(request, pk):
    packing = get_object_or_404(Packing, id=pk)
    invoice = packing.invoice
    context = {"packing":packing,
                "invoice":invoice, 
                "translations":get_translation(invoice)}
    return render(request,'packing_print.html', context)

def print_tag(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    context = {"invoice":invoice, 
                "translations":get_translation(invoice)}
    return render(request,'tag_print.html', context)

def update_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if  form.is_valid():
            form.save()
            update_orders(request)
            messages.success(request, 'Invoice has been created successfully')
        else:
            messages.error(request, get_message_error(form))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'invoice_edit.html',  context=invoice_detail(invoice))

def invoice_detail(invoice):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    return {'invoice':invoice,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings}

def add_article_to_invoice(request, invoice_pk, article_nbr):
    try:
        invoice = Invoice.objects.get(id=invoice_pk)
        article = Article.objects.get(article_nbr=article_nbr)
        order = Order(article=article, quantity=1, margin=0, 
                      purchase_price=article.purchase_price, 
                      invoice=invoice)
        order.save()
    except Article.DoesNotExist or invoice.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article or offer not found'})
    context = invoice_detail(invoice)
    return render(request, 'invoice_edit.html',context)

def delete_order_from_invoice(request, pk):
    order = get_object_or_404(Order, pk=pk)
    invoice = order.invoice
    order.delete()
    return render(request, 'invoice_edit.html', context=invoice_detail(invoice))