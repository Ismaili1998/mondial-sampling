from django.contrib import admin
from .models import Language, Country, Representative,Buyer \
    , Currency, Shipping, Transport, Destination, Payment, \
    Client, Supplier, Bank_info, Project, TimeUnit

admin.site.site_header = 'Mondial-sampling Administration'
admin.site.site_title = 'Mondial-sampling Administration'


class projectAdmin(admin.ModelAdmin):
    list_display = (
        'project_nbr',
        'project_name',
    )
    search_fields = ['project_nbr','project_name',]

class RepresentativeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone_number'
    )
    search_fields = ['name']

class BuyerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone_number'
    )
    search_fields = ['name']

class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'language_name',
        'language_code',
    )
    search_fields = ['language_name', 'language_code']


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'country_name_fr',
    )
    search_fields = ['country_name_en', 'country_name_fr']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
    )
    search_fields = ['symbol']

class ShippingAdmin(admin.ModelAdmin):
    list_display = (
        'term',
    )
    search_fields = ['term']

class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'mode',
    )
    search_fields = ['mode']

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'mode',
    )
    search_fields = ['mode']

class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        'destination_name',
    )
    search_fields = ['destination_name']

class TimeUnitAdmin(admin.ModelAdmin):
    list_display = (
        'unit_name',
    )
    search_fields = ['unit_name']

class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'client_nbr',
        'client_name',
    )
    search_fields = ['client_nbr', 'client_name']

class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'supplier_name',
    )
    search_fields = ['supplier_name']

admin.site.register(Project, projectAdmin)
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(TimeUnit, TimeUnitAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(Bank_info)


