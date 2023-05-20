from django.db import models
from client.models import Client
from client.models import Country
from client.models import Language
import datetime

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

    def get_infos_text(self):
        language_code = self.supplier.language.language_code
        if language_code == "en":
            return """Reseller, please max reduction.
                +We ask for your offer including the following informations as soon as possible
                +- Pricing: ex works, including domestic packaging and freight to our addres.
                +- Validity of the offer: at least 90 days
                +- Delivery time
                +- approximate total weight / volume:
                +- Customs tariff number(s) (HS-Code):
                +- Country of origin:
                +- Dangerous goods for air or sea freight: yes / no:""".split("+")

        elif language_code == "de" :
            return """Wiederverkäufer, bitte max. Rabatte (Exportprojekt)
            +wir bitten um Ihr Angebot einschließlich folgender Angaben schnellst möglich
            +- Preisstellung:ab Werk, einschl. Inlandsverpackung
            +- Angebotsgültigkeit:mindestens 90 Tage
            +- Lieferzeit:
            +- ungefähres Gesamtgewicht/ -volumen:
            +- Zolltarifnummer(n):
            +- Ursprungsland:
            +- Gefahrgut für Luft- oder Seefracht: ja / nein:""".split("+")
        
        else:
            return """Veuillez nous consentir le max. de reduction (Projet d'export).
            +Nous vous demandons votre offre comprenant les informations suivantes dès que possible:
            +- Prix : départ usine, y compris l'emballage domestique et frais jusqu'à notre adresse.
            +- Validité de l'offre : au moins 90 jours
            +- Délai de livraison:
            +- Poids / Volume total approximatif:
            +- Numéro(s) de tarif douanier:
            +- Pays d'origine:
            +- Marchandises dangereuses pour le fret aérien ou maritime : oui / non :""".split("+")

    def get_greeting_text(self):
        language_code = self.supplier.language.language_code
        if language_code == "en":
            return "Dear Sirs,"
        elif language_code == "de":
            return "Sehr geehrte,"
        else:
            return "Messieurs,"
    
    def get_controlling_idea_text(self):
        language_code = self.supplier.language.language_code
        if language_code == "en":
            return "Please provide us urgently with your best price and delivery time for:"
        elif language_code == "de":
            return "Damen und Herrn, erbeten Ihr günstigstes Angebot in aller Eile über:"
        else:
            return "Veuillez nous transmettre en toute urgence votre meilleure offre et delai pour:"
    
    def get_signature_text(self):
        language_code = self.supplier.language.language_code
        if language_code == "en":
            return "Best regards"
        elif language_code == "de":
            return "Mit freundlichen Grüßen"
        else:
            return "Meilleures Salutations"

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
    offer_nbr = models.CharField(max_length=20) 
    project = models.ForeignKey(Project,on_delete=models.PROTECT)
    transport = models.ForeignKey(Transport,on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT)
    destination = models.ForeignKey(Destination,on_delete=models.PROTECT)
    delivery_time_interval = models.CharField(max_length=20)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.PROTECT) 
    articles = models.ManyToManyField(Article)
    duration_in_days = models.IntegerField() 
    validity_date = models.DateField() 
    customs_fee = models.DecimalField(max_digits=12, decimal_places=2) 
    transport_fee = models.DecimalField(max_digits=12, decimal_places=2) 

    class Meta:
        db_table = 'commercial_offer'

    def __str__(self):
        return self.offer_nbr
    
    def get_total_purchase(self):
        total_purchase = 0
        for article in self.articles:
            total_purchase += article.quantity * article.purchase

    def get_total_selling(self):
        total_selling = 0
        for article in self.articles:
            total_selling += article.quantity * article.selling_price
    
    def get_validate_date(self):
        current_date = datetime.date.today()
        future_date = current_date + datetime.timedelta(days=self.duration_in_days)
        return future_date 


    def get_greeting_text(self):
        language_code = self.project.client.language.language_code
        if language_code == "en":
            return "Dear Sirs,"
        elif language_code == "de":
            return "Sehr geehrte,"
        else:
            return "Messieurs,"
    
    def get_controlling_idea_text(self):
        language_code = self.project.client.language.language_code
        if language_code == "en":
            return """We refer to your consultation, for which we thank you very much 
            and are pleased to send you our offer as follows:"""
        elif language_code == "de":
            return """Wir verweisen auf Ihre Beratung, für die wir uns sehr bedanken und die wir Ihnen gerne 
            zukommen lassen Unser Angebot wie folgt:"""
        else:
            return """ Nous nous référons à votre consultation, pour laquelle nous vous remercions 
            vivement et avons le plaisir de vous transmettre notre offre comme suit:"""
        
    def get_signature_text(self):
        language_code = self.project.client.language.language_code
        if language_code == "en":
            return "Best regards"
        elif language_code == "de":
            return "Mit freundlichen Grüßen"
        else:
            return "Meilleures Salutations"




