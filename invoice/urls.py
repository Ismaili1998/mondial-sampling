from django.urls import path
from . import views

urlpatterns = [
    path('create-invoice/<str:offer_pk>',views.create_invoice,name='create-invoice'),
    path('print-invoice/<str:pk>',views.print_invoice,name='print-invoice'),
    path('delete-invoice/<str:pk>',views.delete_invoice,name='delete-invoice'),

    path('print-customsReport/<str:pk>',views.print_customsReport,name='print-customsReport'),

    path('create-packing/<str:invoice_pk>',views.create_packing,name='create-packing'),
    path('update-packing/<str:pk>',views.update_packing,name='update-packing'),
    path('print-packing/<str:pk>',views.print_packing,name='print-packing'),
    
    path('print-tag/<str:pk>',views.print_tag, name='print-tag'),
]
