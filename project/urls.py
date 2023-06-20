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
    path('upload-file-to-project/<str:project_pk>',views.upload_file_to_project,name='upload-file-to-project'),
    path('download-file/<str:file_pk>',views.download_file,name='download-file'),





    path('create-article',views.article_create,name='create-article'),
    path('update-article/<str:pk>',views.article_edit,name='update-article'),
    path('get-article/<str:article_nbr>',views.article_detail,name='article-detail'),
    path('delete-article/<str:pk>',views.article_delete,name='delete-article'),
    path('get-articlesByKeyWord',views.get_articlesByKeyWord,name='get-articlesByKeyWord'),
    path('add-article-to-project',views.add_article_to_project ,name='add-article-to-project'),



    path('create-supplier',views.supplier_create,name='create-supplier'),

    path('create-quoteRequest/<str:project_pk>', views.create_quoteRequest, name='create-quoteRequest'),
    path('create-quoteRequest-pdfReport/<str:request_pk>', views.create_quoteRequest_pdfReport, name='create-quoteRequest-pdfReport'),

    path('create-commercialOffer/<str:project_pk>', views.create_commercialOffer, name='create-commercialOffer'),
    path('update-commercialOffer/<str:pk>', views.update_commercialOffer, name='update-commercialOffer'),
    path('create-commercialOffer-pdfReport/<str:offer_pk>/', views.create_commercialOffer_pdfReport, name='create-commercialOffer-pdfReport'),
    path('print-technicalOffer/<str:offer_pk>/', views.print_technicalOffer, name='print-technicalOffer'),

]

