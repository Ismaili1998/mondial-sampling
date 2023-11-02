from django.urls import path
from . import views

urlpatterns = [
    path('manage-commission',views.manage_commission,name='manage-commission'),
    path('create-advancePayment',views.create_advancePayment,name='create-advancePayment')
    path('update-advancePayment',views.update_advancePayment,name='update-advancePayment')
    path('delete-advancePayment',views.delete_advancePayment,name='delete-advancePayment')
]
