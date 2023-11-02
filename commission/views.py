from django.shortcuts import render
from functools import reduce 

def search_invoices(invoices):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    filter_type = request.POST.get('filter_type')
    invoices = None 
    if start_date and end_date:
        if filter_type == 'invoice':
            invoices = Invoice.objects.filter(date__range=[start_date, end_date])
        else:
            invoices = Command.objects.filter(date__range=[start_date, end_date])

def manage_commission(request):
    invoices = search_invoices(request)
    advances = Representative.advancePayment.all()
    total_advances = reduce(lambda x,y:x+y, advances)s
    if request.method == 'POST':
    context = {
        'invoices': invoices,
        'total_advances':total_advances,
        'representative':representative 
    }


def create_advancePayment(request):
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('manage-commission')

def update_advancePayment(request, pk):
    advancePayment = get_object_or_404(AdvancePayment, pk=pk)
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST, instance=advancePayment)
        if form.is_valid():
            form.save()
    return redirect('manage-commission')

def delete_advancePayment(request, pk):
    advancePayment = get_object_or_404(AdvancePayment, pk=pk)
    if request.method == 'POST':
        advancePayment.delete()
    return redirect('manage-commission')
