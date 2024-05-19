from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from order.models import Article
from project.models import Client, Supplier
from quoteRequest.models import QuoteRequest
from commercialOffer.models import CommercialOffer
from commercialOffer.models import Confirmed_commercialOffer
from invoice.models import Invoice
from django.shortcuts import render, redirect, get_object_or_404



def manage_search(request):
    keyword = request.GET.get('keyword')
    filter_type = request.GET.get('filter_type') or 'client'
    context = {"keyword":keyword, "filter_type":filter_type}
    if keyword:
        if filter_type == 'client':
            context[filter_type]  = get_object_or_404(Client, client_nbr=keyword)
            context['commercialOffers'] = CommercialOffer.objects.filter(project__client__client_nbr=keyword)[:50]  
            context['confirmedOffers'] = Confirmed_commercialOffer.objects.filter(project__client__client_nbr=keyword)[:50]  
            context['invoices'] = Invoice.objects.filter(project__client__client_nbr=keyword)[:50]                                         
        elif filter_type == 'article':
            context[filter_type]  = get_object_or_404(Article, article_nbr=keyword)
        elif filter_type == 'supplier':
            context[filter_type] = get_object_or_404(Supplier, supplier_nbr=keyword)
    return render(request, f'search_by_{filter_type}.html', context)
