from django.shortcuts import render, redirect, get_object_or_404
from functools import reduce 
from client.models import Representative
from project.models import Confirmed_commercialOffer
from django.contrib import messages
from .forms import AdvancePaymentForm
from django.utils import timezone
from datetime import datetime
from .models import AdvancePayment

def get_representativeInvoices(request):
    if request.GET:
        start_date = request.GET.get('start_date')
        request.session['start_date'] = start_date 
        end_date = request.GET.get('end_date')
        request.session['end_date'] = end_date 
        representative_pk= request.GET.get('representative')
        request.session['representative_pk'] = representative_pk
        filter_type = request.GET.get('filter_type')
        request.session['filter_type'] = filter_type
    else:
        start_date = request.session['start_date']
        end_date = request.session['end_date']
        representative_pk = request.session['representative_pk']
        filter_type = request.session['filter_type']
    
    invoices = representative = {}
    if representative_pk:
        representative = get_object_or_404(Representative, id=representative_pk)
    if start_date and end_date and representative:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)
        if filter_type == 'invoice':
            invoices = Confirmed_commercialOffer.objects.filter(created_at__range=[start_date, end_date], 
                                                                commercialOffer__project__client__representative=representative)
        else:
            invoices = Confirmed_commercialOffer.objects.filter(created_at__range=[start_date, end_date], 
                                                                commercialOffer__project__client__representative=representative)
    return  representative, invoices 

def get_context(request):
    representative, invoices =  get_representativeInvoices(request)
    advancePayments = representative.advancepayment_set.all() if representative else None 
    total_advances = 0 
    for advance in advancePayments:
        total_advances += advance.amount
    total_commissions = 0
    total_sales = 0
    for invoice in invoices:
        total_commissions += invoice.get_commission()
        total_sales += invoice.commercialOffer.get_total_selling_withFee()
    context = {
        "representatives":Representative.objects.all(),
        'invoices': invoices,
        "advancePayments":advancePayments,
        "remaining":total_advances - total_commissions,
        'total_advances':total_advances,
        "total_sales":total_sales,
        "total_commission":total_commissions,
        'representative':representative 
    }
    
    return context

def manage_commission(request):
    context = get_context(request)
    return render(request, 'commission.html', context)


def create_advancePayment(request):
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST)
        if form.is_valid():
            a = form.save()
            messages.success(request, 'Payment advance has been modified successfully !')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
    return redirect('manage-commission')

def update_advancePayment(request, pk):
    advancePayment = get_object_or_404(AdvancePayment, pk=pk)
    print(advancePayment)
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST, instance=advancePayment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment advance has been modified successfully !')
        else:
            messages.error(request, 'An error occured, please retry')
    context = get_context(request)
    context['advancePayment'] = advancePayment
    return render(request, 'commission.html', context)

def delete_advancePayment(request, pk):
    advancePayment = get_object_or_404(AdvancePayment, pk=pk)
    advancePayment.delete()
    messages.success(request, 'Payment advance has been modified successfully !')
    return redirect('manage-commission')


def print_commission(request):
    context = get_context(request)
    return render(request, 'commission_print.html', context)