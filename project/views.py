from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, Supplier_contactForm, ClientForm
from .models import Project, Supplier, Client, Country, Language, File, Local_contact, Client_contact, Representative
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from django.http import Http404
from django.contrib.auth.decorators import login_required
from order.models import Article 

@login_required(login_url='sign-in')
def project_home(request):
    clients = Client.objects.all()
    latest_project = Project.objects.order_by('-id').first()
    last_id = latest_project.id if latest_project else 0 
    project_nbr  = "A{0}".format(last_id + 1)
    local_contacts = Local_contact.objects.all()
    client_contacts = Client_contact.objects.all()
    context = {'clients':clients,
               'page':'add-project',
               'local_contacts': local_contacts,
               'client_contacts': client_contacts,
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr=project_nbr)
    clients = Client.objects.all()
    articles = project.article_set.all()[:50]
    page_name = 'update-project'
    local_contacts = Local_contact.objects.all()
    client_contacts = Client_contact.objects.all()
    context = {'project':project,
               'clients':clients, 
               'local_contacts':local_contacts,
               'client_contacts': client_contacts,
               'page':page_name,
               'articles':articles}
    return render(request, 'project_home.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been created successfully')
            return project_detail(request,project.project_nbr)
        for err in form.errors:
            print(err)
        messages.error(request, 'An error occured, please retry')
    return redirect('project-home')

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been updated successfully')
    return redirect('project-detail', project.project_nbr)


def project_delete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request, 'project has been deleted successfully')
    return redirect('project_home')

def add_article_to_project(request):
    if request.method == 'POST':
        project_nbr = request.POST['project_nbr']
        article_nbr = request.POST['article_nbr']
        try:
            project = Project.objects.get(project_nbr=project_nbr)
            article = Article.objects.get(article_nbr=article_nbr)
            article.project = project
            article.save()
            messages.success(request,'Article has been added to project succesfully')
        except:
            messages.error(request,'An error occured ! please retry again')
        return redirect('project-detail', project_nbr)

def remove_article_from_project(request, article_pk):
    article = Article.objects.get(id=article_pk)
    project = article.project 
    article.project = None
    article.save()
    messages.success(request,'Article has been removed from project succesfully')
    return redirect('project-detail', project.project_nbr)
  
@csrf_exempt
def get_projectsByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    projects = Project.objects.filter(project_nbr__icontains=keyword).values_list('project_nbr', flat=True)[:20]
    return JsonResponse(list(projects), safe=False)

def upload_file_to_project(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('files')
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

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    countries = Country.objects.all()
    page_name = 'update-client'
    context = {'client':client,'countries':countries,'page':page_name}
    return render(request, 'client.html', context)

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Client has been added successfully'})
        
        for err in form.errors:
            print(err)
        return JsonResponse({'message':'An error occured ! please retry again'})
    page_name = 'add-client'
    nbr_clients = Client.objects.all().count()
    client_nbr  = "C{0}".format(nbr_clients + 1)
    countries = Country.objects.all()
    languages = Language.objects.all()
    representatives = Representative.objects.all()
    context = {'client_nbr':client_nbr,
               'countries':countries,
               'languages':languages,
               'representatives':representatives,
               'page':page_name}
    return render(request, 'client.html', context)

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Client has been modified successfully'})
        
        for err in form.errors:
            print(err)
        return JsonResponse({'message':'An error occured ! please retry again'})
    
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

def client_delete(request, pk):
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
            return JsonResponse({'message': 'Client has been added successfully'})
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
    suppliers = Supplier.objects.filter(supplier_name__icontains=keyword)[:5]
    # Prepare the suppliers' data for JSON serialization
    supplier_data = []
    if len(suppliers):
        for supplier in suppliers:
            supplier_data.append({
                'id': supplier.id,
                'supplier_name': supplier.supplier_name or '',
                'supplier_nbr':supplier.supplier_nbr,
                'country': ''
            })

    # Return the suppliers' data as JSON response
    return JsonResponse({'suppliers': supplier_data})







