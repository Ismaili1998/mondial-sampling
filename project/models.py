from django.db import models
from client.models import Client, Country, Language, Payment, Transport, Currency, Shipping, Local_contact

class Supplier(models.Model):
    supplier_nbr = models.CharField(max_length=30, null=True)
    supplier_name = models.CharField(max_length=150,null=True)
    
    email = models.EmailField(unique=True,null=True, blank= True)
    phone_number = models.CharField(max_length=40,null=True, blank=True)
    fax = models.CharField(max_length=40,blank=True,null=True)    
    address = models.CharField(max_length=200,blank=True,null=True)
    postal_code = models.CharField(max_length=50,blank=True,null=True)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=150,blank=True, null=True)
    language = models.ForeignKey(Language,on_delete=models.PROTECT,null=True,blank=True)
    delivery_type = models.CharField(max_length=100,blank=True,null=True)
    comment = models.TextField(blank=True, max_length=500,null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'Supplier'
        ordering = ['-id']
    
    def __str__(self):
        return self.supplier_name

class Supplier_contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null= True)
    phone_number = models.CharField(max_length=20, blank=True, null= True)
    supplier = models.OneToOneField(Supplier, on_delete=models.PROTECT, blank=True, null= True)


    class Meta:
        db_table = 'Supplier_contact'
        
    def __str__(self) -> str:
        return self.name 
    
class ArticleUnit(models.Model):
    unit_name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = 'Article_unit'
              

class Client_contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null= True, blank=True)
    phone_number = models.CharField(max_length=40, blank=True, null= True)

    class Meta:
        db_table = 'Client_contact'
        
    def __str__(self) -> str:
        return self.name 
    
class Project(models.Model):
    #required fields 
    project_nbr = models.CharField(max_length=30, unique=True)
    project_name = models.CharField(max_length=150, null= True)
    our_ref = models.CharField(max_length=50,null=True)

    #optional fields 
    client_ref = models.CharField(max_length=50,null=True, blank=True)
    project_description = models.TextField(blank=True,max_length=500, null= True)
    to_do = models.TextField(blank=True,max_length=500, null= True)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    local_contact =  models.ForeignKey(Local_contact,on_delete=models.PROTECT,null=True,blank=True)
    client_contact =  models.ForeignKey(Client_contact,on_delete=models.PROTECT,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null= True)

    
    class Meta:
        db_table = 'Project'

    def __str__(self):
        return self.project_name


class Article(models.Model):
    article_nbr = models.CharField(max_length=30,unique=True)
    description_de = models.TextField(null= True, max_length=1500)
    description_fr = models.TextField(null= True, max_length=1500)
    description_en = models.TextField(null= True, max_length=1500)

    article_name = models.CharField(max_length=150,null=True, blank= True)
    project = models.ForeignKey(Project,on_delete=models.PROTECT,null=True,blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    article_unit = models.ForeignKey(ArticleUnit,on_delete=models.PROTECT,null=True, blank= True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    customs_tariff =  models.CharField(max_length=150, null= True, blank= True)
    customs_description = models.TextField(blank=True, max_length=500, null= True)
    comment = models.TextField(blank=True, max_length=500, null= True)

    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null= True)

    def __str__(self):
        return self.article_nbr
    
    class Meta:
        db_table = 'Article'
        ordering = ['-created_at']

   
    def get_description(self):
        language_code = 'fr'
        try:
            language_code = self.project.client.language.language_code
        except:
            pass 
        if  self.project.client.language:
            language_code = self.project.client.language.language_code
        if language_code == 'fr':
            return self.description_fr
        elif language_code == 'en':
            return self.description_en
        elif language_code == 'de':
            return self.description_de
        else:
            return self.description_fr
    
    
        
class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')
    description = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'File'
    

class QuoteRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    request_nbr = models.CharField(max_length=20,unique=True)
    articles = models.ManyToManyField(Article)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        db_table = 'QuoteRequest'
        ordering = ['-id']
    
class Destination(models.Model):
    destination_name = models.CharField(max_length=150)
    class Meta:
        db_table = 'Destination'
    
    def __str__(self) -> str:
        return self.destination_name

class TimeUnit(models.Model):
    unit_name = models.CharField(max_length=20) #days, weeks, months ...
    class Meta:
        db_table = 'Time_unit'
    
    def __str__(self) -> str:
        return self.unit_name
    

class CommercialOffer(models.Model):
    offer_nbr = models.CharField(max_length=20, unique=True) 
    project = models.ForeignKey(Project,on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)
    margin = models.DecimalField(max_digits=4, decimal_places=2) 
    articles = models.ManyToManyField(Article)

    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True,null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.PROTECT, blank=True,null=True)
    transport = models.ForeignKey(Transport,on_delete=models.PROTECT, blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT, blank=True,null=True)
    local_contact = models.BooleanField(default=1)
    destination = models.ForeignKey(Destination,on_delete=models.PROTECT, blank=True,null=True)
    delivery_time_interval = models.CharField(max_length=20, blank=True,null=True)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.PROTECT, blank=True,null=True) 
    duration_in_days = models.IntegerField(blank=True,null=True) 
    validity_date = models.DateField(blank=True,null=True)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True,null=True) 
    transport_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True,null=True) 

    class Meta:
        db_table = 'Commercial_offer'

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
    
   
class Buyer(models.Model):
    name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    phone_number = models.CharField(max_length=20, blank=True, null= True)
    project = models.OneToOneField(Project, on_delete=models.PROTECT,null=True,unique=False)

    class Meta:
        db_table = 'Buyer'

    def __str__(self) -> str:
        return self.name






