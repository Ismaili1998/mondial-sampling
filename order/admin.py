from django.contrib import admin
from .models import Article, ArticleUnit
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': 
                ('purchase_price', 'article_nbr', 'description_fr', 'description_de', 'description_en','article_unit','hs_code')}),
    ]
    
    list_display = (
        'article_nbr',
    )
    search_fields = ['article_nbr', 'description_fr', 'description_de', 'description_en']

class ArticleUnitAdmin(admin.ModelAdmin):
    list_display = (
        'unit_name',
    )
    search_fields = ['unit_name']

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleUnit, ArticleUnitAdmin)