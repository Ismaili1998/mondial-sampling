from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, Supplier_contactForm,ClientForm, BuyerForm
from .models import Project, Supplier, Client, Country, Language, File, Representative, Buyer, Representative
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from django.http import Http404
from order.models import Article 
import os 
from datetime import datetime

def get_project_nbr():
    P_PREFIX = 'P'
    last_rank = 0
    latest_project = Project.objects.order_by('-id').first()
    current_year = datetime.now().strftime("%y")
    if latest_project and latest_project.rank is not None and \
    latest_project.project_nbr.startswith(f'{P_PREFIX}{current_year}'):
        last_rank = latest_project.rank + 1
        project_nbr = f'{P_PREFIX}{current_year}{last_rank:04d}'
    else:
        project_nbr = f'{P_PREFIX}{current_year}{last_rank:04d}'
    return last_rank, project_nbr

def project_home(request):
    _, project_nbr  = get_project_nbr()
    representatives = Representative.objects.all()
    context = {'representatives': representatives,
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, pk):
    try:
        project = Project.objects.get(id=pk)
        Representatives = Representative.objects.all()
        context = {'project':project,
                   'representatives':Representatives}
    except Project.DoesNotExist:
        messages.error(request, 'Project not found !')
    return render(request, 'project_home.html', context)

def get_message_error(form):
    errors = form.errors.as_data()
    custom_errors = ""
    for field, field_errors in errors.items():
        for error in field_errors:
            custom_errors += f"Error in field '{field}': {error.message}\n"
    return custom_errors

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            last_rank,_  = get_project_nbr()
            project.rank = last_rank
            project.save()
            messages.success(request, 'Project has been created successfully')
            return redirect('project-detail', project.id)
        messages.error(request, get_message_error(form))
    return redirect('project-home')

def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been updated successfully')
        else:
            messages.error(request, get_message_error(form))
    return redirect('project-detail', project.id)


def delete_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request, 'project has been deleted successfully')
    return redirect('project_home')

def add_article_to_project(request):
    if request.method == 'POST':
        project_nbr = request.POST.get('project_nbr')
        article_nbr = request.POST.get('article_nbr')
        try:
            project = Project.objects.get(project_nbr=project_nbr)
            article = Article.objects.get(article_nbr=article_nbr)
            article.projects.add(project)
            messages.success(request, 'Article has been added to project successfully.')
            return redirect('project-detail', project.id)
        except Project.DoesNotExist:
            messages.error(request, f"Project with number '{project_nbr}' not found.")
        except Article.DoesNotExist:
            messages.error(request, f"Article with number {article_nbr} not found.")
        except Exception as e:
            messages.error(request, f"Unexpected error occurred, please retry later !")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def remove_article_from_project(request, project_pk, article_pk):
    article = Article.objects.get(id=article_pk)
    project = Project.objects.get(id=project_pk)
    if request.method == "POST": 
        article.projects.remove(project)
        messages.success(request,'Article has been removed from project succesfully')
    return redirect('project-detail', project.id)
  
@csrf_exempt
def get_projectsByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    projects = Project.objects.filter(project_nbr__icontains=keyword).values('id', 'project_nbr')[:20]
    return JsonResponse(list(projects), safe=False)

@csrf_exempt
def get_clientsByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    projects = Client.objects.filter(client_nbr__icontains=keyword).values('id','client_nbr')[:20]
    return JsonResponse(list(projects), safe=False)

def upload_file_to_project(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    if len(project.file_set.all()) > 10:
        return JsonResponse({'message': 'No more than 10 files !'})
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('files')
        if len(files) > 10:
            return JsonResponse({'message': 'No more than 10 files !'})
        filenames = []
        for file in files:
            project_file = File(project=project,
                                       file=file,
                                       description="")
            project_file.save()
            filenames.append(project_file.file.name)
        return JsonResponse({'message': 'files have been added successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'})

def download_file(request, file_pk):
    try:
        project_file = File.objects.get(id=file_pk)
    except File.DoesNotExist:
        raise Http404
    # Use Django's built-in `serve()` view to return the file
    return serve(request, project_file.file.name, document_root=settings.MEDIA_ROOT)

def remove_file(request, file_pk):
    if request.method == 'POST':
        try:
            project_file = File.objects.get(id=file_pk)
            if project_file:
                project_file.delete()
        except:
            messages.error(request,'Error occured !')
        return redirect('project-detail',project_file.project.id)

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message':'Client has been created successfully'})
        return JsonResponse({'message':get_message_error(form)})
    countries = Country.objects.all()
    languages = Language.objects.all()
    representatives = Representative.objects.all()
    page_name = 'add-client'
    context = {'countries':countries,
               'languages':languages,
               'representatives':representatives,
               'page':page_name}
    return render(request, 'client.html', context)

def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Client has been modified successfully'})
        return JsonResponse({'message': get_message_error(form)})
    countries = Country.objects.all()
    page_name = 'update-client'
    representatives = Representative.objects.all()
    languages = Language.objects.all()
    context = {'client':client,
               'countries':countries,
               'representatives':representatives,
               'languages':languages,
               'page':page_name}
    return render(request, 'client.html', context)

def get_clientByRef(request, ref):
    try:
        client = Client.objects.get(client_nbr=ref)
    except Client.DoesNotExist:
        return JsonResponse({'message':'Client not found !'})
    countries = Country.objects.all()
    page_name = 'update-client'
    representatives = Representative.objects.all()
    languages = Language.objects.all()
    context = {'client':client,
               'countries':countries,
               'representatives':representatives,
               'languages':languages,
               'page':page_name}
    return render(request, 'client.html', context)

def delete_client(request, pk):
    if request.method == "POST":
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        messages.success(request, 'project has been deleted successfully')
        return redirect('client-list')

def supplier_create(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier = supplier_form.save()
            supplier_contact_form =Supplier_contactForm(prefix='supplier_contact', data=request.POST)
            if supplier_contact_form.is_valid():
                supplier_contact = supplier_contact_form.save(commit=False)
                supplier_contact.supplier = supplier 
                supplier_contact.save()
            else:
                for field, errors in supplier_contact_form.errors.items():
                    for error in errors:
                        print(f"Field: {field} - Error: {error}")
            return JsonResponse({'message': 'Client has been added successfully'})
        else:
            for err in supplier_form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
    
    countries = Country.objects.all()
    page_name = 'add-supplier'
    languages = Language.objects.all()
    context = {'countries':countries,
               'page':page_name,
               'languages':languages}
    return render(request, 'supplier.html',context)

def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST, instance=supplier)
        if supplier_form.is_valid():
            supplier = supplier_form.save()
            try:
                supplier_contact_form = Supplier_contactForm(prefix='supplier_contact',
                                                            data=request.POST, 
                                                            instance=supplier.supplier_contact)
                if supplier_contact_form.is_valid():
                    supplier_contact = supplier_contact_form.save(commit=False)
                    supplier_contact.supplier = supplier 
                    supplier_contact.save()
                else:
                    for field, errors in supplier_contact_form.errors.items():
                        for error in errors:
                            print(f"++Field: {field} - Error: {error}")
            except:
                pass
                supplier_contact_form = Supplier_contactForm(prefix='supplier_contact',
                                                            data=request.POST)
                if supplier_contact_form.is_valid():
                    supplier_contact = supplier_contact_form.save(commit=False)
                    supplier_contact.supplier = supplier 
                    supplier_contact.save()
                else:
                    for field, errors in supplier_contact_form.errors.items():
                        for error in errors:
                            print(f"Field: {field} - Error: {error}")
            return JsonResponse({'message': 'Supplier has been updated successfully'})
        else:
            for err in supplier_form.errors:
                print(err)
            return JsonResponse({'message':'An error occured ! please retry again'})
        
    countries = Country.objects.all()
    page_name = 'update-supplier'
    languages = Language.objects.all()
    context = {'countries':countries,
               'page':page_name,
               'supplier':supplier,
               'languages':languages}
    return render(request, 'supplier.html',context)
        
def get_suppliersByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    # Perform the search query using the keyword
    supplier_data = Supplier.objects.filter(supplier_name__icontains=keyword) \
    .values('id','supplier_name','country')[:10]
    # Return the suppliers' data as JSON response
    return JsonResponse({'suppliers': list(supplier_data)})


@csrf_exempt
def get_buyersByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    buyers = Buyer.objects.filter(name__icontains=keyword).values('id','name','email','phone_number')[:5]
    return JsonResponse(list(buyers), safe=False)

def create_buyer(request): 
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            buyer = form.save()
            buyer = {
                'id': buyer.id,
                'name': buyer.name,
            }
            return JsonResponse({'buyer': buyer})
        return JsonResponse({'error': get_message_error(form)})
    return render(request, 'buyer.html')

def update_buyer(request, pk):
    buyer = get_object_or_404(Buyer, id=pk) 
    if request.method == 'POST':
        form = BuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            buyer = form.save()
            buyer = {
                'id': buyer.id,
                'name': buyer.name,
            }
            return JsonResponse({'buyer': buyer})
        return JsonResponse({'error': get_message_error(form)})
    context = {'buyer': buyer}
    return render(request, 'buyer.html', context)



