
from django.urls import path
from . import views

urlpatterns = [
    path('create-quoteRequest/<str:project_pk>', views.create_quoteRequest, name='create-quoteRequest'),
    path('add-article-to-quoteRequest/<str:request_pk>/<str:article_nbr>', views.add_article_to_quoteRequest, name='add-article-to-quoteRequest'),
    path('delete-order-from-quoteRequest/<str:pk>', views.delete_order_from_quoteRequest, name='delete-order-from-quoteRequest'),
    path('update-quoteRequest/<str:pk>', views.update_quoteRequest, name='update-quoteRequest'),
    path('delete-quoteRequest/<str:pk>', views.delete_quoteRequest, name='delete-quoteRequest'),
    path('create-quoteRequest-pdfReport/<str:request_pk>', views.create_quoteRequest_pdfReport, name='create-quoteRequest-pdfReport'),

    path('supplier-command/<str:request_pk>/', views.supplier_command, name='supplier-command'),
    path('print-supplierCommand/<str:pk>/', views.print_supplierCommand, name='print-supplierCommand'),
    path('update-supplierCommand/<str:pk>/', views.update_supplierCommand, name='update-supplierCommand'),
    path('delete-supplierCommand/<str:pk>/', views.delete_supplierCommand, name='delete-supplierCommand'),
]