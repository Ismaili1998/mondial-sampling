from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from project.models import Project, TimeUnit, Destination, Currency, Shipping, Transport, Payment
from project import translations
from .models import CommercialOffer, Confirmed_commercialOffer
from .forms import CommercialOfferForm, Confirmed_commercialOfferForm
from order.models  import Article, Order 
import re

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
               'shippings': shippings,
               'orders':commercialOffer.order_set.all()}

def create_commercialOffer(request,project_pk):
    project = get_object_or_404(Project, id=project_pk)
    project_nbr = project.project_nbr
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST)
        if form.is_valid():
            offers = project.commercialoffer_set.all()
            index = 1
            if len(offers):
                last_offer = offers.order_by('-id').first()
                offer_nbr = last_offer.offer_nbr
                pattern = r'G(\d+)-'
                index = int(re.search(pattern, offer_nbr).group(1)) + 1      
            project_nbr = project.project_nbr
            client_nbr = project.client.client_nbr
            offer_nbr = "{0}/G{1}-{2}".format(project_nbr, index, client_nbr)
            commercialOffer = form.save(commit=False)
            commercialOffer.offer_nbr = offer_nbr
            commercialOffer.confirmation_nbr = offer_nbr.replace('G', 'C')
            commercialOffer.save()

            articles = request.POST.getlist('article')
            quantities = request.POST.getlist('quantity')
            margins = request.POST.getlist('article-margin')
            purchase_prices = request.POST.getlist('purchase-price')
            for article, quantity, margin, purchase_price in zip(articles, quantities, margins, purchase_prices):
                order = Order(article_id=article, quantity=quantity,
                              purchase_price = purchase_price, 
                              margin=margin, commercialOffer=commercialOffer)
                order.save()
            messages.success(request, 'Commercial offer has been created successfully')
            return redirect('project-detail', project_nbr)
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    # Print or log the error details
                    print(f"Field: {field}, Error: {error.message}")
            messages.error(request, 'An error occured, please retry')
            return redirect('project-detail', project.project_nbr)
        
    article_ids = request.GET.getlist('articles[]')
    try:
        articles = Article.objects.filter(id__in=article_ids)
    except Article.DoesNotExist:
            messages.error(request, 'An error occured, please retry') 
            return redirect('project-detail', project.project_nbr) 

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

def update_commercialOffer(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if request.method == 'POST':
        project = commercialOffer.project
        form = CommercialOfferForm(request.POST,instance=commercialOffer)
        if form.is_valid():
            form.save()
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
            messages.success(request, 'Commercial offer has been updated successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', project.project_nbr)
    
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    context = {'commercialOffer':commercialOffer,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings,
               'orders':commercialOffer.order_set.all()}
    return render(request, 'commercialOffer_edit.html',context) 

def add_article_to_commercialOffer(request, offer_pk, article_nbr):
    try:
        commercialOffer = get_object_or_404(CommercialOffer, id=offer_pk)
        article = get_object_or_404(Article, article_nbr=article_nbr)
        order = Order(article=article, quantity=1, margin=0, 
                      purchase_price=article.purchase_price, 
                      commercialOffer=commercialOffer)
        order.save()
    except Article.DoesNotExist or CommercialOffer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article or offer not found'})
    timeUnits = TimeUnit.objects.all()
    payments = Payment.objects.all()
    transports = Transport.objects.all()
    destinations = Destination.objects.all()
    currencies = Currency.objects.all()
    shippings = Shipping.objects.all()
    context = {'commercialOffer':commercialOffer,
               'currencies': currencies,
               'timeUnits':timeUnits,
               'payments':payments,
               'transports':transports,
               'destinations':destinations,
               'shippings': shippings,
               'orders':commercialOffer.order_set.all()}
    return render(request, 'commercialOffer_edit.html',context)

def delete_commercialOffer(request, pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=pk)
    project = commercialOffer.project 
    if request.method == 'POST':
        commercialOffer.delete()
        messages.success(request, 'commercial offer has been deleted successfully')
    return redirect('project-detail',project.project_nbr)

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
        if commercialOffer.confirmed:
            messages.error(request, 'Offer already confirmed !')
            return redirect('project-detail', commercialOffer.project.project_nbr)
        confirmedOffer = Confirmed_commercialOfferForm(request.POST)
        if  confirmedOffer.is_valid():
            commercialOffer.confirmed = True
            commercialOffer.save()
            confirmedOffer = confirmedOffer.save(commit=False)
            confirmedOffer.confirmation_nbr = commercialOffer.offer_nbr.replace('G','C') 
            confirmedOffer.commercialOffer = commercialOffer
            confirmedOffer.save()
            messages.success(request, 'Project has been created successfully')
        else:
            messages.error(request, 'An error occured, please retry')
        return redirect('project-detail', commercialOffer.project.project_nbr)
    
    context = {"commercialOffer":commercialOffer}
    return render(request, 'confirme_commercialOffer.html', context)

def cancel_confirmedOrder(request,pk):
    commercialOffer = get_object_or_404(CommercialOffer, id=pk)
    if commercialOffer.confirmed:
        commercialOffer.confirmed = False
        confirmedOffer = commercialOffer.confirmed_commercialoffer
        confirmedOffer.delete()
        commercialOffer.save()
    return redirect('project-detail', commercialOffer.project.project_nbr)

def print_technicalOffer(request, offer_pk):
    commercialOffer = get_object_or_404(CommercialOffer, pk=offer_pk)
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer, 'translations':filtered_translations}
    return render(request, 'technicalOffer_print.html', context)

def print_confirmedOrder(request, offer_pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, pk=offer_pk)
    commercialOffer = confirmedOffer.commercialOffer
    language_code = 'fr'
    try:
        language_code = commercialOffer.project.client.language.language_code 
    except:
        pass 
    filtered_translations = {key:value[language_code] for key, value in translations.translations.items()}
    context = {'commercialOffer':commercialOffer,
               'confirmedOffer':confirmedOffer, 
               'translations':filtered_translations}
    return render(request, 'confirmedOrder_print.html', context)


def delete_order_from_commercialOffer(request, pk):
    order = get_object_or_404(Order, pk=pk)
    commercialOffer = order.commercialOffer 
    order.delete()
    return render(request, 'commercialOffer_edit.html', commercialOffer_detail(commercialOffer))


def update_confirmed_commercialOffer(request, pk):
    confirmedOffer = get_object_or_404(Confirmed_commercialOffer, id=pk)
    commercialOffer = confirmedOffer.commercialOffer
    if request.method == 'POST':
        confirmedOffer = Confirmed_commercialOfferForm(request.POST, instance=confirmedOffer)
        if  confirmedOffer.is_valid():
            confirmedOffer.save()
            messages.success(request, 'Confirmed offer has been created successfully')
            return redirect('project-detail', commercialOffer.project.project_nbr)
    context = {"commercialOffer":commercialOffer,
               "confirmedOffer":confirmedOffer
               }
    return render(request, 'confirmed_commercialOffer_edit.html', context)