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
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email1 = models.EmailField()
    email2 = models.EmailField()
    website = models.URLField()
    internal_contact = models.CharField(max_length=200)
    external_contact = models.CharField(max_length=200)
    representative = models.CharField(max_length=200)
    representative_1 = models.CharField(max_length=200)
    representative_2 = models.CharField(max_length=200)
    language = models.CharField(max_length=200, choices=[
        ('English', 'English'),
        ('German', 'German'),
        ('French', 'French'),
    ])
    
    credit_limit = models.FloatField()
    remark = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.client_name
    