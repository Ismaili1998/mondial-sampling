from django.shortcuts import render, redirect, get_object_or_404
from functools import reduce 
from project.models import Representative
from commercialOffer.models import Confirmed_commercialOffer
from django.contrib import messages
from .forms import AdvancePaymentForm
from django.utils import timezone
from datetime import datetime
from .models import AdvancePayment

def get_representativeInvoices(request):
    invoices = representative = None 
    if request.GET:
        # get filters data  
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        representative_pk= request.GET.get('representative')
        filter_type = request.GET.get('filter_type')
        # store filters data into session 
        search_filters = {}
        search_filters['start_date'] = start_date 
        search_filters['end_date'] = end_date 
        search_filters['representative_pk'] = representative_pk
        search_filters['filter_type'] = filter_type
        request.session['search_filters'] = search_filters
    else:
        if "search_filters" in request.session:
            search_filters = request.session['search_filters']
            start_date = search_filters['start_date']
            end_date = search_filters['end_date']
            representative_pk = search_filters['representative_pk']
            filter_type = search_filters['filter_type']

        else:
            return  representative, invoices
    if start_date and end_date and representative_pk:
        representative = get_object_or_404(Representative, id=representative_pk)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)
        if filter_type == 'invoice':
            invoices = Confirmed_commercialOffer.objects.filter(created_at__range=[start_date, end_date], 
                                                                commercialOffer__project__representative=representative)
        else:
            invoices = Confirmed_commercialOffer.objects.filter(created_at__range=[start_date, end_date], 
                                                                commercialOffer__project__representative=representative)
    return  representative, invoices 

def get_context(request):
    representative, invoices =  get_representativeInvoices(request)
    advancePayments = None
    total_advances = total_commissions = total_sales = 0 
    if representative:
        advancePayments = representative.advancepayment_set.all()
        for advance in advancePayments:
            total_advances += advance.amount
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
        'representative':representative,
        'search_filters':request.session['search_filters'] if "search_filters" in request.session else None,
    }
    return context

def manage_commission(request):
    context = get_context(request)
    context['form_name'] = "create"
    return render(request, 'commission.html', context)


def create_advancePayment(request):
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST)
        if form.is_valid():
            advance = form.save()
            messages.success(request, f'Payment advance has been added successfully to : {advance.representative}')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
    return redirect('manage-commission')

def update_advancePayment(request, pk):
    advancePayment = get_object_or_404(AdvancePayment, pk=pk)
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST, instance=advancePayment)
        if form.is_valid():
            form.save()  # This should update the existing record
            messages.success(request, 'Payment advance has been modified successfully !')
            return redirect('manage-commission')
        else:
            messages.error(request, 'An error occurred, please retry')

    # Assuming get_context is a function defined elsewhere
    context = get_context(request)
    context['form_name'] = "update"
    context['advancePayment'] = advancePayment
    return render(request, 'commission.html', context)

    # Make sure to return the context or an HTTP response at the end of your view function
    # For example:
    # return render(request, 'your_template.html', context)


def delete_advancePayment(request, pk):
    advancePayment = get_object_or_404(AdvancePayment, pk=pk)
    advancePayment.delete()
    messages.success(request, 'Payment advance has been deleted successfully !')
    return redirect('manage-commission')


def print_commission(request):
    context = get_context(request)
    return render(request, 'commission_print.html', context)