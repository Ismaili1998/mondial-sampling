from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=4)

    def __str__(self):
        return self.country_name +" "+self.abbreviation        
    
    class Meta:
        db_table = 'country'


class Client(models.Model):
    client_name = models.CharField(max_length=100)
    client_nbr = models.CharField(max_length=50,unique=True)
    address = models.CharField(max_length=200,blank=True)
    postal_code = models.CharField(max_length=20,blank=True)
    city = models.CharField(max_length=200)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email1 = models.EmailField(unique=True)
    email2 = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    internal_contact = models.CharField(max_length=200,blank=True)
    external_contact = models.CharField(max_length=200,blank=True)
    representative = models.CharField(max_length=200,blank=True)
    representative_1 = models.CharField(max_length=200,blank=True)
    representative_2 = models.CharField(max_length=200,blank=True)
    language = models.CharField(max_length=200)
    
    credit_limit = models.FloatField(blank=True)
    remark = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.client_name
    