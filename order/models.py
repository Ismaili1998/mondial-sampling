from django.db import models
from commercialOffer.models import CommercialOffer
from quoteRequest.models import QuoteRequest
from project.models import Project

class ArticleUnit(models.Model):
    unit_name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = 'article_unit'

class Article(models.Model):
    article_nbr = models.CharField(max_length=30,unique=True)
    description_de = models.TextField(null= True, max_length=1500)
    description_fr = models.TextField(null= True, max_length=1500)
    description_en = models.TextField(null= True, max_length=1500)

    project = models.ForeignKey(Project,on_delete=models.PROTECT,null=True,blank=True)
    article_unit = models.ForeignKey(ArticleUnit,on_delete=models.PROTECT,null=True, blank= True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    hs_code =  models.CharField(max_length=150, null= True, blank= True)
    customs_description = models.TextField(blank=True, max_length=500, null= True)
    comment = models.TextField(blank=True, max_length=500, null= True)

    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null= True)

    def __str__(self):
        return self.article_nbr
    
    class Meta:
        db_table = 'article'
        ordering = ['-created_at']

   
    def get_description(self, language_code):
        if language_code == 'en':
            return self.description_en
        elif language_code == 'de':
            return self.description_de
        return self.description_fr

class Order(models.Model):
    article = models.ForeignKey(Article,on_delete=models.PROTECT)
    commercialOffer = models.ForeignKey(CommercialOffer,on_delete=models.CASCADE,null=True)
    quoteRequest = models.ForeignKey(QuoteRequest,on_delete=models.CASCADE,null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    margin = models.DecimalField(max_digits=4, decimal_places=2,  null= True, blank=True)

    class Meta:
        db_table = 'order'
        ordering = ['-id']

    def __str__(self):
        return "{0} of {1}".format(self.quantity, self.article.article_name)

    def get_selling_price(self):
        return ((self.margin / 100) * self.get_total_price()) or 0
    
    def get_total_price(self):
        return (self.article.purchase_price * self.quantity) or 0
    
    def get_description_by_client_lang(self):
        language_code = self.commercialOffer.project.client.language.language_code
        return self.article.get_description(language_code) or ''
    
    def get_description_by_supplier_lang(self):
        language_code = self.quoteRequest.project.client.language.language_code
        return self.article.get_description(language_code) or ''
