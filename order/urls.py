from django.urls import path
from . import views

urlpatterns = [
    path('create-article/<str:project_pk>',views.create_article,name='create-article'),
    path('update-article/<str:pk>',views.update_article,name='update-article'),
    path('get-article/<str:article_nbr>',views.article_detail,name='article-detail'),
    path('get-articleByKeyWord',views.get_articlesByKeyWord,name='get-articleByKeyWord'),
    path('delete-order/<str:pk>',views.article_detail ,name='delete-order'),
    
]

