from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from invoice.models import Invoice
from quoteRequest.models import SupplierCommand

def get_payment_filters(request):
    if request.GET:
        # Get filter data
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        nbr_days = request.GET.get('nbr_days')
        filter_type = request.GET.get('filter_type')
        # Store filter data into session
        payment_filters = {
            'start_date': start_date,
            'end_date': end_date,
            'nbr_days': nbr_days,
            'filter_type': filter_type
        }
        request.session['payment_filters'] = payment_filters
    else:
        payment_filters = request.session.get('payment_filters', None)

    return payment_filters

def filter_invoices(start_date, end_date, nbr_days):
    current_date = timezone.now()
    future_date = current_date + timedelta(days=int(nbr_days))
    return Invoice.objects.filter(commercialOffer__payment_date__gte=current_date, 
                                  commercialOffer__payment_date__lte=future_date)

def filter_supplierCommands(start_date, end_date, nbr_days):
    current_date = timezone.now()
    future_date = current_date + timedelta(days=int(nbr_days))
    return SupplierCommand.objects.filter(payment_date__gte=current_date, 
                                          payment_date__lte=future_date)

def manage_payment(request):
    payment_filters = get_payment_filters(request)
    if not payment_filters:
        return render(request, 'income.html')
    
    start_date = payment_filters['start_date']
    end_date = payment_filters['end_date']
    nbr_days = payment_filters['nbr_days']
    filter_type = payment_filters['filter_type']

    if filter_type == 'expense':
        supplierCommands = filter_supplierCommands(start_date, end_date, nbr_days)
        total_cost = sum(command.get_final_total() for command in supplierCommands)
        context = {
            'supplierCommands': supplierCommands,
            'total_cost': total_cost,
            'payment_filters': payment_filters,
        }
        return render(request, 'cost.html', context)

    else:
        invoices = filter_invoices(start_date, end_date, nbr_days)
        total_sales = sum(invoice.commercialOffer.get_total_selling_withFee() for invoice in invoices)
        context = {
            'invoices': invoices,
            'total_sales': total_sales,
            'payment_filters': payment_filters,
        }
        return render(request, 'income.html', context)
   
