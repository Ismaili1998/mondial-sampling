from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.project_home,name='project-home'),
    path('create-project',views.project_create,name='create-project'),
    path('get-project/<str:project_nbr>',views.project_detail,name='project-detail'),
    path('update-project/<str:pk>',views.project_edit,name='update-project'),
    path('delete-project/<str:pk>',views.project_delete,name='delete-project'),
    path('get-projectsByKeyWord',views.get_projectsByKeyWord,name='get-projectsByKeyWord'),


    path('create-article',views.article_create,name='create-article'),
    path('update-article/<str:pk>',views.article_edit,name='update-article'),
    path('get-article/<str:article_nbr>',views.article_detail,name='article-detail'),
    path('delete-article/<str:pk>',views.article_delete,name='delete-article'),
    path('get-articlesByKeyWord',views.get_articlesByKeyWord,name='get-articlesByKeyWord'),
    path('add-article-to-project',views.add_article_to_project ,name='add-article-to-project'),


    path('create-commercial-offer',views.commercial_offer_create,name='create-commercial-offer'),

    path('create-supplier',views.supplier_create,name='create-supplier'),

    path('manage-quoteRequest/<str:project_pk>/<str:article_pk>/', views.manage_quoteRequest, name='manage-quoteRequest'),

]

