from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from project.models import Project, TimeUnit, Destination, \
Currency, Shipping, Transport, Payment
from project import translations
from .models import CommercialOffer, Confirmed_commercialOffer
from .forms import CommercialOfferForm, Confirmed_commercialOfferForm
from order.models  import Article, Order 
from project.views import get_message_error

def commercialOffer_detail(commercialOffer):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    return {'commercialOffer':commercialOffer,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings}

def confirmedOffer_detail(confirmedOffer):
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    return {'confirmedOffer':confirmedOffer,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings}

def create_commercialOffer_orders(request, commercialOffer):
    articles = request.POST.getlist('article')
    quantities = request.POST.getlist('quantity')
    margins = request.POST.getlist('article-margin')
    purchase_prices = request.POST.getlist('purchase-price')
    for article, quantity, margin, purchase_price in zip(articles, quantities, margins, purchase_prices):
        order = Order(article_id=article, quantity=quantity,
                        purchase_price = purchase_price, 
                        margin=margin, commercialOffer=commercialOffer)
        order.save()

def get_rank(offers):
    rank = 1
    if len(offers):
        last_offer = offers.order_by('-rank').first()
        rank = last_offer.rank + 1
    return rank 

def create_commercialOffer(request,project_pk):
    project = get_object_or_404(Project, id=project_pk)
    project_nbr = project.project_nbr
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST)
        if form.is_valid():
            offers = project.commercialoffer_set.all()
            rank = get_rank(offers)
            client_nbr = project.client.client_nbr
            commercialOffer = form.save(commit=False)
            commercialOffer.rank = rank
            commercialOffer.offer_nbr = "{0}/G{1}-{2}".format(project_nbr, rank, client_nbr)
            commercialOffer.save()
            create_commercialOffer_orders(request, commercialOffer)
            messages.success(request, 'Commercial offer has been created successfully')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, get_message_error(form))
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    article_ids = request.GET.getlist('articles[]')
    try:
        articles = Article.objects.filter(id__in=article_ids)
    except Article.DoesNotExist:
            messages.error(request, 'An error occured, please retry') 
            return redirect(request.META.get('HTTP_REFERER', '/')) 
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    context = {'project':project,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings':shippings,
               'articles':articles}
    return render(request, 'commercialOffer_create.html',context) 


def update_orders(request):
    order_ids = request.POST.getlist('order')
    quantities = request.POST.getlist('quantity')
    margins = request.POST.getlist('article-margin')
    purchase_prices = request.POST.getlist('purchase-price')
    for order_id, quantity, margin,  purchase_price in zip(order_ids, quantities, margins, purchase_prices):
        order = get_object_or_404(Order, id=order_id)
        order.quantity = quantity
        order.margin = margin
        order.purchase_price = purchase_price
        order.save()

def update_commercialOffer(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST,instance=commercialOffer)
        if form.is_valid():
            form.save()
            update_orders(request)
            messages.success(request, 'Commercial offer has been updated successfully')
        else:
            messages.error(request, get_message_error(form))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    context = commercialOffer_detail(commercialOffer)
    return render(request, 'commercialOffer_edit.html',context) 

def add_article_to_commercialOffer(request, offer_pk, article_nbr):
    try:
        commercialOffer = CommercialOffer.objects.get(id=offer_pk)
        article = Article.objects.get(article_nbr=article_nbr)
        order = Order(article=article, quantity=1, margin=0, 
                      purchase_price=article.purchase_price, 
                      commercialOffer=commercialOffer)
        order.save()
    except Article.DoesNotExist or CommercialOffer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article or offer not found'})
    context = commercialOffer_detail(commercialOffer)
    return render(request, 'commercialOffer_edit.html',context)


def add_article_to_confirmedOffer(request, offer_pk, article_nbr):
    try:
        confirmedOffer = Confirmed_commercialOffer.objects.get(id=offer_pk)
        article = Article.objects.get(article_nbr=article_nbr)
        order = Order(article=article, quantity=1, margin=0, 
                      purchase_price=article.purchase_price, 
                      confirmed_commercialOffer=confirmedOffer)
        order.save()
    except Article.DoesNotExist or CommercialOffer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article or offer not found'})
    context = confirmedOffer_detail(confirmedOffer)
    return render(request, 'confirmed_commercialOffer_edit.html',context)

def delete_commercialOffer(request, pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=pk)
    project = commercialOffer.project
    if request.method == 'POST':
        commercialOffer.delete()
        messages.success(request, 'commercial offer has been deleted successfully')
    return redirect('project-detail',project.id)

def print_commercialOffer(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'commercialOffer_print.html', context)

def confirm_commercialOffer(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if request.method == 'POST':
        form = Confirmed_commercialOfferForm(request.POST)
        project = commercialOffer.project
        project_nbr = project.project_nbr
        if  form.is_valid():
            confirmedOffer = form.save(commit=False)
            confirmed_offers = project.confirmed_commercialoffer_set.all()
            rank = get_rank(confirmed_offers)
            client_nbr = project.client.client_nbr
            confirmedOffer.confirmation_nbr = "{0}/C{1}-{2}".format(project_nbr, rank, client_nbr)
            confirmedOffer.rank = rank
            confirmedOffer.save()
            confirmedOffer.clone_orders_from_commercialOffer(commercialOffer)
            messages.success(request, 'Offer has been confirmed successfully')
        else:
            messages.error(request, get_message_error(form))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    context = {"commercialOffer":commercialOffer}
    return render(request, 'confirm_commercialOffer.html', context)

def cancel_confirmedOffer(request,pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, pk=pk)
    project = confirmedOffer.project
    if request.method == 'POST':
        confirmedOffer.delete()
        messages.success(request, 'confirmed offer has been canceled successfully')
    return redirect('project-detail',project.id)

def print_technicalOffer(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        language_code = 'fr'
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'technicalOffer_print.html', context)

def print_confirmedOffer(request, offer_pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, pk=offer_pk)
    try:
        language_code = confirmedOffer.project.client.language.language_code 
    except:
        language_code = 'fr'
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'confirmedOffer':confirmedOffer, 
               'translations':filtered_translations}
    return render(request, 'confirmedOrder_print.html', context)


def delete_order_from_commercialOffer(request, pk):
    order = get_object_or_404(Order, pk=pk)
    commercialOffer = order.commercialOffer 
    order.delete()
    return render(request, 'commercialOffer_edit.html', context=commercialOffer_detail(commercialOffer))

def delete_order_from_confirmedOffer(request, pk):
    order = get_object_or_404(Order, pk=pk)
    confirmedOffer = order.confirmed_commercialOffer 
    order.delete()
    return render(request, 'confirmed_commercialOffer_edit.html', context=confirmedOffer_detail(confirmedOffer))

def update_confirmed_commercialOffer(request, pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, id=pk)
    if request.method == 'POST':
        form = Confirmed_commercialOfferForm(request.POST, instance=confirmedOffer)
        if  form.is_valid():
            form.save()
            update_orders(request)
            messages.success(request, 'Confirmed offer has been created successfully')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    context = confirmedOffer_detail(confirmedOffer)
    return render(request, 'confirmed_commercialOffer_edit.html', context)