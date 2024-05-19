from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from order.models import Article
from project.models import Client, Supplier
from quoteRequest.models import QuoteRequest
from commercialOffer.models import CommercialOffer
from commercialOffer.models import Confirmed_commercialOffer
from django.shortcuts import render


def get_filters(request):
    if request.GET:
        # get filters data  
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        keyword= request.GET.get('keyword')
        filter_type = request.GET.get('filter_type')
        # store filters data into session 
        search_engine_filters = {}
        search_engine_filters['start_date'] = start_date 
        search_engine_filters['end_date'] = end_date 
        search_engine_filters['keyword'] = keyword
        search_engine_filters['filter_type'] = filter_type
        request.session['search_engine_filters'] = search_engine_filters

    elif "search_engine_filters" in request.session:
        search_engine_filters = request.session['search_engine_filters']
        start_date = search_engine_filters['start_date']
        end_date = search_engine_filters['end_date']
        keyword = search_engine_filters['keyword']
        filter_type = search_engine_filters['filter_type']

    return search_engine_filters


def get_objects_by_filterType(search_engine_filters):
    start_date = search_engine_filters['start_date']
    end_date = search_engine_filters['end_date']
    keyword = search_engine_filters['keyword']
    filter_type = search_engine_filters['filter_type']
    if start_date and end_date and keyword:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)
        if filter_type == 'client':
            return Client.objects.filter(Q(created_at__range=[start_date, end_date]) &
                                            (Q(client_nbr__icontains = keyword) |
                                            Q(client_name__icontains = keyword))
                                            )[:10]
                                                
        elif filter_type == 'article':
            return Article.objects.filter(Q(created_at__range=[start_date, end_date]) &
                                            (Q(article_nbr__icontains = keyword) |
                                            Q(article_name__icontains = keyword))
                                            )[:10]
        else:
            return Supplier.objects.filter(Q(created_at__range=[start_date, end_date]) &
                                            (Q(supplier_nbr__icontains = keyword) |
                                            Q(supplier_name__icontains = keyword))
                                            )[0]
    return 


def manage_search(request):
    context = {}
    filter_type = "client"
    search_engine_filters = get_filters(request)
    if search_engine_filters:
        print(search_engine_filters)
        filter_type = search_engine_filters['filter_type']
        context[filter_type] = get_objects_by_filterType(search_engine_filters)
        context['search_engine_filters'] = search_engine_filters
    return render(request, f'search_by_{filter_type}.html', context)
