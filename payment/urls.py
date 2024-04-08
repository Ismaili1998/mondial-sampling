from django.urls import path
from . import views

urlpatterns = [
    path('manage-payment',views.manage_payment,name='manage-payment'),
]
