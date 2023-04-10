from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, ArticleForm, QuoteRequestForm
from .models import Project, Supplier, Article, QuoteRequest, Unit
from client.models import Client, Country
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def project_home(request):
    clients = Client.objects.all()
    nbr_projects = Project.objects.all().count()
    project_nbr  = "P{0}".format(nbr_projects + 1)
    context = {'clients':clients,
               'page':'add-project',
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)

def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr = project_nbr)
    clients =Client.objects.all()
    articles = project.article_set.all()
    quoteRequests = QuoteRequest.objects.all()
    page_name = 'update-project'
    context = {'project':project,
               'clients':clients, 
               'page':page_name,
               'articles':articles,
               'quoteRequests':quoteRequests}
    return render(request, 'project_home.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project has been created successfully')
        else:
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
            messages.success(request, 'Project has been modified successfully')
        else:
            messages.error(request, 'An error occured, please retry')
    else:
        form = ProjectForm(instance=project)
    return redirect('project-detail', project.project_nbr)


def project_delete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request, 'project has been deleted successfully')
    return redirect('project_home')

@csrf_exempt
def get_projectsByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    projects = Project.objects.filter(project_nbr__icontains=keyword).values_list('project_nbr', flat=True)
    return JsonResponse(list(projects), safe=False)

#======================= Article area ====================================#
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, 'Article has been created successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        return redirect('project-home')
    
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    units = Unit.objects.all()
    article_nbr = Article.objects.all().count()
    article_nbr = "A{0}".format(article_nbr)
    page_name = 'add-article'
    context = {'projects':projects, 
               'suppliers':suppliers,
               'units':units,
               'article_nbr':article_nbr,
               'page':page_name}
    return render(request, 'article.html',context)

def article_detail(request, article_nbr):
    article= get_object_or_404(Article, article_nbr = article_nbr)
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    context = {'article':article, 'projects':projects, 'suppliers':suppliers}
    return render(request, 'article.html', context)

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article has been modified successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        project_nbr = article.project.project_nbr
        return redirect('project-detail',project_nbr)
    
    page_name = 'update-article'
    projects = Project.objects.all()
    suppliers = Supplier.objects.all()
    units = Unit.objects.all()
    context = {'article':article, 
               'projects':projects, 
               'suppliers':suppliers,
               'units':units,
               'page':page_name}
    return render(request, 'article.html', context)

def article_delete(request, pk):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        messages.success(request, 'Article has been deleted successfully')
    return redirect('project-home')

#======================= supplier area ====================================#
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier has been created successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        
        return redirect('project-home')
    countries = Country.objects.all()
    page_name = 'add-supplier'
    context = {'countries':countries,'page':page_name}
    return render(request, 'supplier.html',context) 

#======================= quoteRequest area ====================================#
def manage_quoteRequest(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.quoteRequest is not None:
        return quoteRequest_edit(request,article)
    return quoteRequest_create(request,article)

def quoteRequest_create(request,article):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        project = article.project
        if form.is_valid():
            client = project.client
            abbr = client.country.abbreviation
            quoteRequest = form.save(commit=False)
            request_nbr = QuoteRequest.objects.all().count()
            request_nbr  = "{0}-{1}{2}".format(article.article_nbr,abbr,client.client_nbr)
            quoteRequest.request_nbr = request_nbr
            suppliers = form.cleaned_data.get('suppliers')
            quoteRequest.save()
            quoteRequest.suppliers.set(suppliers)
            article.quoteRequest = quoteRequest
            article.save()
            messages.success(request, 'Quote request has been created successfully')
        else:
            print(form.errors)
            messages.error(request, 'An error occured, please retry')
        
        project_nbr = project.project_nbr
        return redirect('project-detail',project_nbr)
    
    suppliers = Supplier.objects.all()
    context = {'article':article,'suppliers':suppliers}
    return render(request, 'quoteRequest.html',context) 

def quoteRequest_edit(request,article):
    quoteRequest = article.quoteRequest
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST, instance=quoteRequest)
        if form.is_valid():
            quoteRequest = form.save(commit=False)
            suppliers = form.cleaned_data.get('suppliers')
            quoteRequest.save()
            quoteRequest.suppliers.set(suppliers)
            messages.success(request, 'quoteRequest has been modified successfully')
        else:
            for err in form.errors:
                print(err)
            messages.error(request, 'An error occured, please retry')
        project_nbr = article.project.project_nbr
        return redirect('project-detail',project_nbr)
    
    suppliers = Supplier.objects.all()
    context = {'article':article, 
               'suppliers':suppliers,}
    return render(request, 'quoteRequest.html', context)

def commercial_offer_create(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')