from django.urls import path
from . import views

urlpatterns = [
    path('manage-commission',views.manage_commission,name='manage-commission'),
    path('create-advancePayment',views.create_advancePayment,name='create-advancePayment'),
    path('update-advancePayment/<str:pk>',views.update_advancePayment,name='update-advancePayment'),
    path('delete-advancePayment/<str:pk>',views.delete_advancePayment,name='delete-advancePayment'),
    path('print-commission',views.print_commission,name='print-commission'),
]
