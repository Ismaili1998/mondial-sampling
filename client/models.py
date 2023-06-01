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

class Currency(models.Model):
    symbol = models.CharField(max_length=2) 
    class Meta:
        db_table = 'Currency'
        
    def __str__(self) -> str:
        return self.symbol
    
class Client(models.Model):
    client_name = models.CharField(max_length=100)
    # transport = models.ForeignKey(Transport,on_delete=models.PROTECT, null=True)
    # payment = models.ForeignKey(Payment,on_delete=models.PROTECT, null=True)
    language = models.ForeignKey(Language,on_delete=models.PROTECT)
    client_nbr = models.CharField(max_length=20,unique=True)
    address = models.CharField(max_length=200,blank=True)
    postal_code = models.CharField(max_length=20,blank=True)
    country = models.ForeignKey(Country,on_delete=models.PROTECT)
    city = models.CharField(max_length=100)
    phone_number1 = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, blank=True)
    email1 = models.EmailField(unique=True)
    email2 = models.EmailField(unique=True,blank=True)
    fax = models.CharField(max_length=20,blank=True)
    website = models.URLField(blank=True)
    internal_contact = models.CharField(max_length=100,blank=True)
    external_contact = models.CharField(max_length=100,blank=True)
    representative = models.CharField(max_length=100,blank=True)
    representative_1 = models.CharField(max_length=100,blank=True)
    representative_2 = models.CharField(max_length=100,blank=True)
    
    credit_limit = models.FloatField(blank=True)
    remark = models.TextField(blank=True,max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.client_name
    