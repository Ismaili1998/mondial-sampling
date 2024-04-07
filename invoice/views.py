from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InvoiceForm, PackingForm
from .models import Invoice, Packing
from project import translations
from commercialOffer.models import Confirmed_commercialOffer

def create_invoice(request, offer_pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, pk=offer_pk)
    if request.method == 'POST':
        commercialOffer = confirmedOffer.commercialOffer
        invoice = InvoiceForm(request.POST)
        if  invoice.is_valid():
            invoice = invoice.save(commit=False)
            invoice.invoice_nbr = commercialOffer.offer_nbr.replace('G','TN') 
            invoice.confirmed_commercialOffer = confirmedOffer
            invoice.save()
            messages.success(request, 'invoice has been created successfully !')
        else:
            messages.error(request, 'an error occured, plase retry !')
        return redirect('project-detail', commercialOffer.project.project_nbr)
    context = {"confirmedOffer":confirmedOffer}
    return render(request, 'create_invoice.html', context)

def print_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.confirmed_commercialOffer.commercialOffer
    context = {'commercialOffer':commercialOffer,
               'invoice':invoice, 
               'translations':get_translation(commercialOffer)}
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
        hs_code = order.article.hs_code  
        if hs_code not in orders_by_hsCode:
            orders_by_hsCode[hs_code] = {"total_quantities": 0, "total_price": 0}
        orders_by_hsCode[hs_code]["total_quantities"] += order.quantity
        orders_by_hsCode[hs_code]["total_price"] += order.get_total_selling()
    return orders_by_hsCode

def get_translation(commercialOffer):
    language = commercialOffer.project.client.language
    language_code = language.language_code if language else "fr" 
    return {key:value[language_code] for key, value in translations.translations.items()}

def print_customsReport(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.confirmed_commercialOffer.commercialOffer
    orders = commercialOffer.order_set.all()
    orders_by_hsCode = calculate_totals_by_hsCode(orders)
    context = {"commercialOffer":commercialOffer,
               "invoice":invoice, 
               "orders_by_hsCode":orders_by_hsCode.items(),
               "translations":get_translation(commercialOffer)}
    return render(request,'customs_report.html', context)

def create_packing(request,invoice_pk):
    invoice = get_object_or_404(Invoice, id=invoice_pk)
    if request.method == 'POST':
        form = PackingForm(request.POST)
        if form.is_valid():
            packing = form.save(commit=False)
            packing.invoice = invoice
            packing.save()
        else:
            messages.error(request, 'an error occured, plase retry !')
        return redirect('project-detail', invoice.confirmed_commercialOffer.commercialOffer.project.project_nbr)
    context = {"invoice":invoice, "form_name":"create"}
    return render(request,'create_packing.html', context)

def update_packing(request, pk):
    packing = get_object_or_404(Packing, id=pk)
    invoice = packing.invoice
    if request.method == 'POST':
        form = PackingForm(request.POST, instance=packing)
        if form.is_valid():
            packing.save()
        else:
            messages.error(request, 'an error occured, plase retry !')
        return redirect('project-detail', invoice.confirmed_commercialOffer.commercialOffer.project.project_nbr)
    context = {"invoice":invoice, 
                "packing":packing, 
                "form_name":"update"}
    return render(request,'create_packing.html', context)


def print_packing(request, pk):
    packing = get_object_or_404(Packing, id=pk)
    invoice = packing.invoice
    commercialOffer = invoice.confirmed_commercialOffer.commercialOffer
    context = {"commercialOffer":commercialOffer,
                "packing":packing,
                "invoice":invoice, 
                "translations":get_translation(commercialOffer)}
    return render(request,'packing_print.html', context)

def print_tag(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.confirmed_commercialOffer.commercialOffer
    context = {"commercialOffer":commercialOffer,
                "invoice":invoice, 
                "translations":get_translation(commercialOffer)}
    return render(request,'tag_print.html', context)

def update_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    commercialOffer = invoice.confirmed_commercialOffer.commercialOffer
    if request.method == 'POST':
        invoice = InvoiceForm(request.POST, instance=invoice)
        if  invoice.is_valid():
            invoice.save()
            messages.success(request, 'Invoice has been created successfully')
        else:
            errors = invoice.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    # Print or log the error details
                    print(f"Field: {field}, Error: {error.message}")
            messages.error(request, 'An error occured, plase retry !')
        return redirect('project-detail', commercialOffer.project.project_nbr)
    
    context = {"commercialOffer":commercialOffer,
               "invoice":invoice
               }
    return render(request, 'invoice_edit.html', context)