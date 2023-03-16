from django.urls import path
from . import views

urlpatterns = [
    path('',views.client_list,name='client-list'),
    path('client_create',views.client_create,name='client-create'),
    path('client_detail/<str:pk>',views.client_detail,name='client-detail'),
    path('client_edit/<str:pk>',views.client_edit,name='client-edit'),
    path('client_delete/<str:pk>',views.client_delete,name='client-delete')
]

