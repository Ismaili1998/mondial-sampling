from django.db import models

class Country(models.Model):
    country_name_fr = models.CharField(max_length=200)
    country_name_en = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=4)

    def __str__(self):
        return self.country_name_fr +" "+self.abbreviation        
    
    class Meta:
        db_table = 'country'
        
class Language(models.Model):
    language_name =  models.CharField(max_length=100)
    language_code =  models.CharField(max_length=4,unique=True)
    
    def __str__(self):
        return self.language_name       

    class Meta:
        db_table = 'language'

class Local_contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=True)

    fax = models.CharField(max_length=50, blank=True, null= True)
    phone_number = models.CharField(max_length=20, blank=True,null=True)

    class Meta:
        db_table = 'local_contact'
        
    def __str__(self) -> str:
        return self.name

class Payment(models.Model):
    mode = models.CharField(max_length=150)
    class Meta:
        db_table = 'payment'
    def __str__(self) -> str:
        return self.mode 

class Transport(models.Model):
    mode = models.CharField(max_length=150) 
    class Meta:
        db_table = 'transport'
    
    def __str__(self) -> str:
        return self.mode
    
class Shipping(models.Model):
    term = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = 'shipping'
    
    def __str__(self):
        return self.term
    
class Currency(models.Model):
    symbol = models.CharField(max_length=2) 
    class Meta:
        db_table = 'currency'
        
    def __str__(self) -> str:
        return self.symbol
    
class Representative(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null= True, blank=True)
    fax = models.CharField(max_length=50, blank=True, null= True)
    phone_number = models.CharField(max_length=40, blank=True, null= True)

    class Meta:
        db_table = 'representative'
        
    def __str__(self) -> str:
        return self.name

class Client(models.Model):
    client_nbr = models.CharField(max_length=30,unique=True)
    client_name = models.CharField(max_length=150, null=True)
    
    representative = models.ForeignKey(Representative,on_delete=models.PROTECT,null= True)
    email1 = models.EmailField(unique=True,null= True, blank= True)
    email2 = models.EmailField(unique=True, null=True, blank=True)
    fax = models.CharField(max_length=40,blank=True,null= True)
    website = models.URLField(blank=True,null= True)
    language = models.ForeignKey(Language,on_delete=models.PROTECT,blank=True,null= True)
    address = models.CharField(max_length=200,null=True,blank=True)
    postal_code = models.CharField(max_length=40,null=True,blank=True)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    phone_number1 = models.CharField(max_length=40,null=True,blank=True)
    phone_number2 = models.CharField(max_length=40,null=True,blank=True)
    credit_limit = models.FloatField(blank=True, null= True)
    comment = models.TextField(max_length=500, null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null= True)

    class Meta:
        db_table = 'client'
        ordering = ['client_nbr']

    def __str__(self):
        return self.client_name

