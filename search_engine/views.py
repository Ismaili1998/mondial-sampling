from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from order.models import Article
from project.models import Client, Supplier
from quoteRequest.models import QuoteRequest, SupplierCommand
from commercialOffer.models import CommercialOffer
from commercialOffer.models import Confirmed_commercialOffer
from invoice.models import Invoice
from django.shortcuts import render, get_object_or_404



def manage_search(request):
    context = {'filter_type':'client', 'keyword':''}
    if request.GET:
        keyword = request.GET.get('keyword')
        filter_type = request.GET.get('filter_type') or 'client'
        context["keyword"] = keyword
        context["filter_type"] = filter_type
        if filter_type == 'client':
            try:    
                client = Client.objects.get(client_nbr=keyword)
                context[filter_type] = client
                context['commercialOffers'] = CommercialOffer.objects.filter(project__client=client)[:50]  
                context['confirmedOffers'] = Confirmed_commercialOffer.objects.filter(project__client=client)[:50]  
                context['invoices'] = Invoice.objects.filter(project__client=client)[:50]                                         
            except Client.DoesNotExist:
                pass
            
        elif filter_type == 'supplier':
            try:
                supplier = Supplier.objects.get(supplier_name=keyword)
                context[filter_type]  = supplier  
                context['supplierCommands'] = SupplierCommand.objects.filter(supplier=supplier)[:50]
                context['quoteRequests'] = QuoteRequest.objects.filter(supplier=supplier)[:50]
            except Supplier.DoesNotExist:
                pass

        elif filter_type == 'article':
            try:
                article = Article.objects.get(article_nbr=keyword)
                context[filter_type] = article
                context['commercialOffers'] = CommercialOffer.objects.filter(order__article=article)[:50]
                context['confirmedOffers'] = Confirmed_commercialOffer.objects.filter(order__article=article)[:50] 
                context['invoices'] = Invoice.objects.filter(order__article=article)[:50]
                context['supplierCommands'] = SupplierCommand.objects.filter(order__article=article)[:50]  
                context['quoteRequests'] = QuoteRequest.objects.filter(order__article=article)[:50]
            except Article.DoesNotExist:
                    pass     
    return render(request, 'commercialOffer_print.html', context)
