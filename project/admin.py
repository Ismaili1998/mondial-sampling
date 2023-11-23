from django.contrib import admin
from .models import Language, Country, Representative, Buyer, Currency, Shipping, Transport, Payment, Client
# Register your models here.
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Representative)
admin.site.register(Currency)
admin.site.register(Shipping)
admin.site.register(Transport)
admin.site.register(Payment)
admin.site.register(Client)

