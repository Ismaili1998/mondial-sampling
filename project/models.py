from django.db import models
from client.models import Client, Country, Language, Payment, Transport, Currency, Shipping

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True)
    postal_code = models.CharField(max_length=50,blank=True)
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
        ordering = ['-id']
    
    def __str__(self):
        return self.supplier_name
    
class ArticleUnit(models.Model):
    unit_name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = 'article_unit'
              
class Article(models.Model):
    article_name = models.CharField(max_length=50)
    article_nbr = models.CharField(max_length=20)
    description_de = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    article_unit = models.ForeignKey(ArticleUnit,on_delete=models.PROTECT,null=True)
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
        ordering = ['-created_at']

   
    def get_description(self):
        language_code = ''
        if language_code == 'fr':
            return self.description_fr
        elif language_code == 'en':
            return self.description_en
        elif language_code == 'de':
            return self.description_de
        else:
            return self.description_fr
 
    
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_nbr = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    articles = models.ManyToManyField(Article, related_name='projects')
    client_ref = models.CharField(max_length=50)
    our_ref = models.CharField(max_length=50)
    project_description = models.TextField(blank=True,max_length=500)
    to_do = models.TextField(blank=True,max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.project_name
    
class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')
    description = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'file'
    

class QuoteRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    request_nbr = models.CharField(max_length=20,unique=True,blank=True)
    articles = models.ManyToManyField(Article)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        db_table = 'quoteRequest'
        ordering = ['-id']
    
class Destination(models.Model):
    destination_name = models.CharField(max_length=150)
    class Meta:
        db_table = 'destination'
    
    def __str__(self) -> str:
        return self.destination_name

class TimeUnit(models.Model):
    unit_name = models.CharField(max_length=20) #days, weeks, months ...
    class Meta:
        db_table = 'time_unit'
    
    def __str__(self) -> str:
        return self.unit_name
    

class CommercialOffer(models.Model):
    offer_nbr = models.CharField(max_length=20, unique=True) 
    project = models.ForeignKey(Project,on_delete=models.PROTECT)
    margin = models.DecimalField(max_digits=4, decimal_places=2) 
    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True,null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    transport = models.ForeignKey(Transport,on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT)
    destination = models.ForeignKey(Destination,on_delete=models.PROTECT)
    delivery_time_interval = models.CharField(max_length=20)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.PROTECT) 
    articles = models.ManyToManyField(Article)
    duration_in_days = models.IntegerField() 
    validity_date = models.DateField() 
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True,null=True) 
    transport_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True,null=True) 

    class Meta:
        db_table = 'commercial_offer'

    def __str__(self):
        return self.offer_nbr
    
    def get_articles(self):
        articles = []
        for article in self.articles.all():
            article.selling_price = round(article.purchase_price + self.margin * article.purchase_price / 100,2)
            article.total_selling_price = round(article.quantity * article.selling_price, 2)
            articles.append(article)
        return articles
    
    def get_total_purchase(self):
        total_purchase = 0
        for article in self.articles.all():
            total_purchase += article.quantity * article.purchase_price
        return round(total_purchase,2)

    def get_total_selling(self):
        total_selling = self.get_total_purchase() + self.get_total_purchase() * self.margin / 100
        return round(total_selling,2)
    
    def get_discounted_price(self):
        if self.discount:
            discounted_price = self.get_total_selling() * (1- self.discount / 100)
            return round(discounted_price,2)
    
    def get_discount_price(self):
        if self.discount:
            discount_price = self.get_total_selling() * (self.discount / 100)
            return round(discount_price,2)


    def get_total_fee(self):
        return (self.transport_fee or 0) + (self.shipping_fee or 0)

    def get_total_selling_withFee(self):
        return (self.get_discounted_price() or self.get_total_selling()) + self.get_total_fee()
    
   





