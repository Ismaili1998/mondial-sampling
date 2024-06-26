
from django.urls import path
from . import views

urlpatterns = [
    path('create-commercialOffer/<str:project_pk>', views.create_commercialOffer, name='create-commercialOffer'),
    path('delete-commercialOffer/<str:pk>', views.delete_commercialOffer, name='delete-commercialOffer'),
    path('update-commercialOffer/<str:pk>', views.update_commercialOffer, name='update-commercialOffer'),
    path('print-commercialOffer/<str:offer_pk>/', views.print_commercialOffer, name='print-commercialOffer'),
    path('add-article-to-commercialOffer/<str:offer_pk>/<str:article_nbr>',views.add_article_to_commercialOffer,name='add-article-to-commercialOffer'),
    path('delete-order-from-commercialOffer/<str:pk>', views.delete_order_from_commercialOffer, name='delete-order-from-commercialOffer'),
    path('print-technicalOffer/<str:offer_pk>/', views.print_technicalOffer, name='print-technicalOffer'),

    path('confirm-commercialOffer/<str:pk>', views.confirm_commercialOffer, name='confirm-commercialOffer'),
    path('add-article-to-confirmedOffer/<str:offer_pk>/<str:article_nbr>',views.add_article_to_confirmedOffer,name='add-article-to-confirmedOffer'),
    path('cancel-confirmedOffer/<str:pk>', views.cancel_confirmedOffer, name='cancel-confirmedOffer'),
    path('delete-order-from-confirmedOffer/<str:pk>', views.delete_order_from_confirmedOffer, name='delete-order-from-confirmedOffer'),
    path('print-confirmedOffer/<str:offer_pk>/', views.print_confirmedOffer, name='print-confirmedOffer'),
    path('update-confirmed-commercialOffer/<str:pk>/', views.update_confirmed_commercialOffer, name='update-confirmed-commercialOffer'),


]