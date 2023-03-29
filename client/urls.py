from django.urls import path
from . import views

urlpatterns = [
    path('',views.client_list,name='client-list'),
    path('create-client',views.client_create,name='create-client'),
    path('client-detail/<str:pk>',views.client_detail,name='client-detail'),
    path('update-client/<str:pk>',views.client_edit,name='update-client'),
    path('delete-client/<str:pk>',views.client_delete,name='delete-client')
]

