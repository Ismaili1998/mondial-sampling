from django.urls import path
from . import views

urlpatterns = [
    path('manage-search',views.manage_search,name='manage-search'),
]
