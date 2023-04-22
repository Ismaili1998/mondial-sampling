from django.db import models
from client.models import Client
from client.models import Country
from client.models import Language

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True)
    postal_code = models.CharField(max_length=10,blank=True)
    country = models.ForeignKey(Country,on_delete=models.PROTECT)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    fax = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=254,unique=True)
    website = models.URLField(max_length=200,blank=True)
    language = models.ForeignKey(Language,on_delete=models.PROTECT,null=True,blank=True)
    supplier_representative = models.CharField(max_length=100,blank=True)
    delivery_type = models.CharField(max_length=100,blank=True)
    internal_representative = models.CharField(max_length=100,blank=True)
    comment = models.TextField(blank=True, max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'
    
    def __str__(self):
        return self.supplier_name
    
class Unit(models.Model):
    unit_name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = 'unit'
              
class Article(models.Model):
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT)
    article_name = models.CharField(max_length=50)
    article_nbr = models.CharField(max_length=20)
    description_de = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit,on_delete=models.PROTECT,null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2)
    customs_tariff =  models.CharField(max_length=150)
    customs_description = models.TextField(blank=True, max_length=500)
    comment = models.TextField(blank=True, max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article_nbr
    
    class Meta:
        db_table = 'article'

    def get_suppliers(self):
        return self.quoterequest_set.values_list('supplier', flat=True)

class QuoteRequest(models.Model):
    request_nbr = models.CharField(max_length=20,unique=True,blank=True)
    articles = models.ManyToManyField(Article)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'quoteRequest'

    def get_description(self):
        if self.supplier.language == 'French':
            return self.article.description_fr
        elif self.supplier.language == 'English':
            return self.article.description_en
        return self.article.description_de

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_nbr = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    articles = models.ManyToManyField(Article, related_name='projects')
    client_ref = models.CharField(max_length=255)
    our_ref = models.CharField(max_length=255)
    project_description = models.TextField(blank=True,max_length=500)
    to_do = models.TextField(blank=True,max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.project_name
# class CommercialOffer(models.Model):
#     pass




