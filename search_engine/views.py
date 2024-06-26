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
        filter_type = request.GET.get('filter_type')
        context["keyword"] = keyword
        context["filter_type"] = filter_type
        if filter_type == 'client':
            clients = Client.objects.filter(Q(client_nbr__icontains=keyword) |
                                            Q(client_name__icontains=keyword))[:20]
            context['clients'] = clients
            return render(request, 'clients_list.html', context)
        elif filter_type == 'supplier':
            suppliers = Supplier.objects.filter(supplier_name__icontains=keyword)[:20]
            context['suppliers'] = suppliers
            return render(request, 'suppliers_list.html', context)
        elif filter_type == 'article':
            articles = Article.objects.filter(Q(article_nbr__icontains=keyword) |
                                              Q(description_en__icontains=keyword) |
                                              Q(description_fr__icontains=keyword) |
                                              Q(description_de__icontains=keyword))[:20]
            context['articles'] = articles
            return render(request, 'articles_list.html', context)
    return render(request, 'clients_list.html', context)
        
def get_supplier_history(request, pk):
    context = {}
    try:
        supplier = Supplier.objects.get(id=pk)
        context['supplierCommands'] = SupplierCommand.objects.filter(supplier=supplier)[:80]
        context['quoteRequests'] = QuoteRequest.objects.filter(supplier=supplier)[:80]
        context["filter_type"] = 'supplier'
    except Supplier.DoesNotExist:
                pass
    return render(request, 'supplier_history.html', context)


def get_client_history(request, pk):
    context = {}
    try:
        client = Client.objects.get(id=pk)
        context['commercialOffers'] = CommercialOffer.objects.filter(project__client=client)[:80]  
        context['confirmedOffers'] = Confirmed_commercialOffer.objects.filter(project__client=client)[:80]  
        context['invoices'] = Invoice.objects.filter(project__client=client)[:80]
        context["filter_type"] = 'client'
    except Client.DoesNotExist:
            pass
    return render(request, 'client_history.html', context)

def get_article_history(request, pk):
    context = {}
    try:
        article = Article.objects.get(id=pk)
        context['commercialOffers'] = CommercialOffer.objects.filter(order__article=article)[:80]
        context['confirmedOffers'] = Confirmed_commercialOffer.objects.filter(order__article=article)[:80] 
        context['invoices'] = Invoice.objects.filter(order__article=article)[:80]
        context['supplierCommands'] = SupplierCommand.objects.filter(order__article=article)[:80]  
        context['quoteRequests'] = QuoteRequest.objects.filter(order__article=article)[:80]
        context["filter_type"] = 'article'
    except Article.DoesNotExist:
            pass
    return render(request, 'article_history.html', context)
