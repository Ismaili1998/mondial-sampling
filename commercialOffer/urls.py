
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
    path('cancel-confirmedOrder/<str:pk>', views.cancel_confirmedOrder, name='cancel-confirmedOrder'),
    path('print-confirmedOrder/<str:offer_pk>/', views.print_confirmOrder, name='print-confirmedOrder'),
    path('update-confirmed-commercialOffer/<str:pk>/', views.update_confirmed_commercialOffer, name='update-confirmed-commercialOffer'),


]