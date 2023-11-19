from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InvoiceForm, PackingForm
from .models import Invoice, Packing
from commercialOffer.models import CommercialOffer
from project.translations import translations

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
