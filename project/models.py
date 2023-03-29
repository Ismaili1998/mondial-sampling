from django.db import models
from client.models import Client
from client.models import Country

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_nbr = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    client_ref = models.CharField(max_length=255)
    our_ref = models.CharField(max_length=255)
    project_description = models.TextField(blank=True)
    to_do = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.project_name

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10,blank=True)
    country = models.ForeignKey(Country,on_delete=models.PROTECT)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField(max_length=254,unique=True)
    website = models.URLField(max_length=200,blank=True)
    supplier_representative = models.CharField(max_length=100,blank=True)
    delivery_type = models.CharField(max_length=100,blank=True)
    internal_representative = models.CharField(max_length=100,blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'
    
    def __str__(self):
        return self.supplier_name

class Article(models.Model):
    project = models.ForeignKey(Project,on_delete=models.PROTECT,null=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT,null=True)
    article_name = models.CharField(max_length=50)
    article_nbr = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    description_de = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2)
    customs_tariff =  models.CharField(max_length=150)
    customs_description = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article_nbr
    
    class Meta:
        db_table = 'article'



