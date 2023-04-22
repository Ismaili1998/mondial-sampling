from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, SupplierForm, ArticleForm, QuoteRequestForm
from .models import Project, Supplier, Article, QuoteRequest, Unit
from client.models import Client, Country, Language
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils

def project_home(request):
    clients = Client.objects.all()
    nbr_projects = Project.objects.all().count()
    project_nbr  = "P{0}".format(nbr_projects + 1)
    context = {'clients':clients,
               'page':'add-project',
               'project_nbr':project_nbr}
    return render(request, 'project_home.html',context)


def project_detail(request, project_nbr):
    project = get_object_or_404(Project, project_nbr=project_nbr)
    clients =Client.objects.all()
    articles = project.articles.all()
    page_name = 'update-project'
    context = {'project':project,
               'clients':clients, 
               'page':page_name,
               'articles':articles}
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
        return redirect('project-home')
    
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

@csrf_exempt
def get_articlesByKeyWord(request):
    keyword = request.GET.get('keyword', '')
    articles = Article.objects.filter(article_nbr__icontains=keyword).values_list('article_nbr', flat=True)
    return JsonResponse(list(articles), safe=False)

def add_article_to_project(request):
    if request.method == 'POST':
        project_nbr = request.POST['project_nbr']
        article_nbr = request.POST['article_nbr']
        try:
            article = Article.objects.get(article_nbr=article_nbr)
            project = Project.objects.get(project_nbr=project_nbr)
            project.articles.add(article)
            project.save()
        except Article.DoesNotExist:
            pass
        return redirect('project-detail', project.project_nbr)
    return redirect('project-home')

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
    languages = Language.objects.all()
    context = {'countries':countries,'page':page_name,'languages':languages}
    return render(request, 'supplier.html',context)

def search_supplier(request):
    if request.method == 'GET':
        # Get the keyword from the request
        keyword = request.GET.get('keyword', '')  
        # Search for suppliers with name containing the keyword
        suppliers = Supplier.objects.filter(name__icontains=keyword)  
        return render(request, 'supplier/search.html', {'suppliers': suppliers, 'keyword': keyword})


#======================= quoteRequest area ====================================#
def manage_quoteRequest(request,project_pk,article_pk):
    project = get_object_or_404(Project, pk=project_pk)
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        client = project.client
        abbr = client.country.abbreviation
        project_nbr = project.project_nbr
        checked_suppliers_ids = request.POST.getlist('suppliers')
        for supplier_id in checked_suppliers_ids:
            try:
                quote_request = QuoteRequest.objects.get(article=article, supplier_id=supplier_id)
                quote_request.request_nbr = 'new_request_number'  # Update with your desired values
                quote_request.save()
            except QuoteRequest.DoesNotExist:
                # Create new QuoteRequest
                quote_request = QuoteRequest(article=article, supplier_id=supplier_id, request_nbr='request_number')
                quote_request.save()
        for index,supplier in enumerate(checked_suppliers,1):
            request_nbr  = "{0}{1}N{2}-{3}{4}".format(project_nbr,article.article_nbr,index,abbr,client.client_nbr)
            quoteRequest = QuoteRequest(supplier=supplier,
                                   article=article,
                                   request_nbr=request_nbr)
            quoteRequest.save()
        messages.success(request, 'Quote request has been created successfully')
        return redirect('project-detail',project_nbr)
    
    suppliers = Supplier.objects.all()
    context = {'project':project,'article':article,'suppliers':suppliers}
    return render(request, 'quoteRequest.html',context) 


def commercial_offer_create(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    # Construct the absolute file path to the PNG image file
    img_path = settings.BASE_DIR / 'static' / 'img' / 'pdf_header.png'
    img = utils.ImageReader(str(img_path))
    # Get the page width and height
    page_width, page_height = A4
    # Calculate the aspect ratio of the image
    img_aspect_ratio = img.getSize()[0] / img.getSize()[1]
    # Calculate the width and height of the image to fit the page width
    img_width = page_width
    img_height = img_width / img_aspect_ratio
    # Calculate the position of the image at the top center of the page
    x = (page_width - img_width) / 2
    y = page_height - img_height
    # Draw the image on the PDF
    p.drawImage(img, x, y, img_width, img_height)
    # Draw other content on the PDF
    p.setFontSize(24)
    p.drawCentredString(page_width / 2, y - 50, "Anstellungsvertrag")
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='demande_devis.pdf')