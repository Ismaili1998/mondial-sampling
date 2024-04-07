from django.urls import path
from . import views
urlpatterns = [
    path('sign-in',views.sign_in,name='sign-in'),
    path('logout',views.log_out,name='logout'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-password',views.update_password,name='update-password')
    
    
    ]