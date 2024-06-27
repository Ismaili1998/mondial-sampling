from django.db import models
from commercialOffer.models import CommercialOffer, Confirmed_commercialOffer
from quoteRequest.models import QuoteRequest, SupplierCommand
from project.models import Project
from invoice.models import Invoice 

class ArticleUnit(models.Model):
    unit_name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=150,blank=True, null=True)
    def __str__(self):
        return self.unit_name or ''

    class Meta:
        db_table = 'article_unit'

class Article(models.Model):
    article_nbr = models.CharField(max_length=30,unique=True)
    description_fr = models.TextField(null=True, max_length=1500)
    description_de = models.TextField(null=True, max_length=1500, blank= True)
    description_en = models.TextField(null=True, max_length=1500, blank= True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    article_unit = models.ForeignKey(ArticleUnit,on_delete=models.SET_NULL,null=True, blank= True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    projects = models.ManyToManyField(Project)
    hs_code =  models.CharField(max_length=150, null= True, blank= True)
    customs_description = models.TextField(blank=True, max_length=500, null= True)
    comment = models.TextField(blank=True, max_length=500, null= True)
    image = models.ImageField(upload_to='article_images/', default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null= True)

    
    class Meta:
        db_table = 'article'
        ordering = ['-created_at']

    def get_description(self, language_code = "fr"):
        if language_code == 'en':
            return self.description_en
        elif language_code == 'de':
            return self.description_de
        return self.description_fr
    
    def __str__(self):
        return self.article_nbr or ''
    

class Order(models.Model):
    article = models.ForeignKey(Article,on_delete=models.PROTECT)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    commercialOffer = models.ForeignKey(CommercialOffer,on_delete=models.CASCADE,null=True)
    confirmed_commercialOffer = models.ForeignKey(Confirmed_commercialOffer,on_delete=models.CASCADE,null=True)
    quoteRequest = models.ForeignKey(QuoteRequest,on_delete=models.CASCADE,null=True)
    confirmed_quoteRequest = models.ForeignKey(SupplierCommand,on_delete=models.CASCADE,null=True)
    purchase_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    margin = models.DecimalField(max_digits=6, decimal_places=2,  default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        return "{0} of {1}".format(self.quantity, self.article.article_name)

    def get_total_selling(self):
        return self.get_total_purchase() * self.margin
    
    def get_total_purchase(self):
        return (self.purchase_price * self.quantity)
    
    def get_selling_price(self):
        return self.purchase_price *  self.margin
    
    def get_description_by_client_lang(self):
        try:
            language_code = self.commercialOffer.project.client.language.language_code
        except:
            language_code = "fr"
        return self.article.get_description(language_code)
    
    def get_description_by_supplier_lang(self):
        try:
            language_code = self.quoteRequest.supplier.language.language_code
        except:
            language_code = "fr"
        return self.article.get_description(language_code)
    
    def __str__(self):
        return f'{self.id}'