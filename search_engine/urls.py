from django.urls import path
from . import views

urlpatterns = [
    path('manage-search',views.manage_search,name='manage-search'),
    path('get-client-history/<str:pk>', views.get_client_history, name='get-client-history'),
    path('get-supplier-history/<str:pk>', views.get_supplier_history, name='get-supplier-history'),
    path('get-article-history/<str:pk>', views.get_article_history, name='get-article-history'),
]
