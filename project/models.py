from django.db import models

class Country(models.Model):
    country_name_fr = models.CharField(max_length=200) #unique=True for country_name
    country_name_en = models.CharField(max_length=200, null=True)
    abbreviation = models.CharField(max_length=4) #unique=True for abb

    def __str__(self):
        return f"{self.country_name_fr} {self.abbreviation}"
            
    class Meta:
        db_table = 'country'
        verbose_name_plural = "Countries"
        
class Language(models.Model):
    language_name =  models.CharField(max_length=100, unique=True)
    language_code =  models.CharField(max_length=4, unique=True)
    
    def __str__(self):
        return self.language_name       

    class Meta:
        db_table = 'language'

class Representative(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null= True, blank=True)
    fax = models.CharField(max_length=50, blank=True, null= True)
    phone_number = models.CharField(max_length=40, blank=True, null= True)

    class Meta:
        db_table = 'representative'
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name or ''
    
class Buyer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null= True, blank=True)
    phone_number = models.CharField(max_length=40, blank=True, null= True)
    
    class Meta:
        db_table = 'buyer'
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name or ''


class Client(models.Model):
    client_nbr = models.CharField(max_length=30,unique=True)
    client_name = models.CharField(max_length=150, null=True) #client_name is unique 
    
    email1 = models.EmailField(null=True, blank=True)
    email2 = models.EmailField(null=True, blank=True)
    fax = models.CharField(max_length=40,blank=True,null= True)
    website = models.URLField(blank=True,null= True)
    language = models.ForeignKey(Language,on_delete=models.SET_NULL,blank=True,null= True)
    address = models.CharField(max_length=200,null=True,blank=True)
    postal_code = models.CharField(max_length=40,null=True,blank=True)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,blank=True)
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
        return self.client_name or ''
      
class Project(models.Model):
    #required fields 
    project_nbr = models.CharField(max_length=30, unique=True)
    project_name = models.CharField(max_length=150, null= True)
    our_ref = models.CharField(max_length=50,null=True)
    #optional fields 
    client_ref = models.CharField(max_length=50,null=True, blank=True)
    project_description = models.TextField(blank=True,max_length=500, null= True)
    to_do = models.TextField(blank=True,max_length=500, null= True)
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null= True)
    representative =  models.ForeignKey(Representative,on_delete=models.SET_NULL,null=True, blank=True)
    buyer =  models.ForeignKey(Buyer,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null= True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.project_name or ''
         
class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')
    description = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'file'
        
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=150)
    supplier_nbr = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank= True)
    phone_number = models.CharField(max_length=40,null=True, blank=True)
    fax = models.CharField(max_length=40,blank=True,null=True)    
    address = models.CharField(max_length=200,blank=True,null=True)
    postal_code = models.CharField(max_length=50,blank=True,null=True)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=150,blank=True, null=True)
    language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True,blank=True)
    delivery_type = models.CharField(max_length=100,blank=True,null=True)
    comment = models.TextField(blank=True, max_length=500,null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'supplier'
        ordering = ['-id']
    
    def __str__(self):
        return self.supplier_name or ''

class Supplier_contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null= True)
    phone_number = models.CharField(max_length=20, blank=True, null= True)
    supplier = models.OneToOneField(Supplier, on_delete=models.SET_NULL, blank=True, null= True)


    class Meta:
        db_table = 'supplier_contact'
        
    def __str__(self) -> str:
        return self.name or ''
    
class Payment(models.Model):
    mode = models.CharField(max_length=150)
    nbr_days = models.IntegerField(null=True, blank=True)
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
        verbose_name_plural = "Currencies"
        
    def __str__(self) -> str:
        return self.symbol
        
class Destination(models.Model):
    destination_name = models.CharField(max_length=150)
    class Meta:
        db_table = 'destination'
    
    def __str__(self) -> str:
        return self.destination_name or ''

class TimeUnit(models.Model):
    unit_name = models.CharField(max_length=20) #days, weeks, months ...
    class Meta:
        db_table = 'time_unit'
    
    def __str__(self) -> str:
        return self.unit_name or ''

class Bank_info(models.Model):
    iban = models.CharField(max_length=200)
    swift = models.CharField(max_length=200)
    haspa = models.CharField(max_length=200)
    customs_code = models.CharField(max_length=200)
    origine = models.CharField(max_length=200)

    class Meta:
        db_table = 'bank_info'
    
    def __str__(self) -> str:
        return self.iban or ''

    
    




