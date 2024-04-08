from django.urls import path
from . import views

urlpatterns = [
    path('create-article',views.article_create,name='create-article'),
    path('update-article/<str:pk>',views.article_edit,name='update-article'),
    path('get-article/<str:article_nbr>',views.article_detail,name='article-detail'),
    path('get-articlesByKeyWord',views.get_articlesByKeyWord,name='get-articlesByKeyWord'),
    path('delete-order/<str:pk>',views.article_detail ,name='delete-order'),
    
]

