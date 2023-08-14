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
    path('add-article-to-commercialOffer/<str:offer_pk>/<str:article_nbr>',views.add_article_to_commercialOffer,name='add-article-to-commercialOffer'),
    path('update-article/<str:pk>',views.article_edit,name='update-article'),
    path('get-article/<str:article_nbr>',views.article_detail,name='article-detail'),
    path('remove-article-from-project/<str:article_pk>',views.remove_article_from_project,name='remove-article-from-project'),
    path('get-articlesByKeyWord',views.get_articlesByKeyWord,name='get-articlesByKeyWord'),
    path('add-article-to-project',views.add_article_to_project ,name='add-article-to-project'),
    path('delete-order/<str:pk>',views.delete_order ,name='delete-order'),



    path('create-supplier',views.supplier_create,name='create-supplier'),
    path('update-supplier/<str:pk>',views.update_supplier,name='update-supplier'),
    path('get-suppliersByKeyWord/', views.get_suppliersByKeyWord, name='get-suppliersByKeyWord'),

    path('create-quoteRequest/<str:project_pk>', views.create_quoteRequest, name='create-quoteRequest'),
    path('add-article-to-quoteRequest/<str:request_pk>', views.add_article_to_quoteRequest, name='add-article-to-quoteRequest'),
    path('remove-article-from-quoteRequest/<str:request_pk>/<str:article_pk>', views.remove_article_from_quoteRequest, name='remove-article-from-quoteRequest'),
    path('update-quoteRequest/<str:pk>', views.update_quoteRequest, name='update-quoteRequest'),
    path('delete-quoteRequest/<str:pk>', views.delete_quoteRequest, name='delete-quoteRequest'),
    path('create-quoteRequest-pdfReport/<str:request_pk>', views.create_quoteRequest_pdfReport, name='create-quoteRequest-pdfReport'),

    path('create-commercialOffer/<str:project_pk>', views.create_commercialOffer, name='create-commercialOffer'),
    path('delete-commercialOffer/<str:pk>', views.delete_commercialOffer, name='delete-commercialOffer'),
    path('update-commercialOffer/<str:pk>', views.update_commercialOffer, name='update-commercialOffer'),
    path('print-commercialOffer/<str:offer_pk>/', views.print_commercialOffer, name='print-commercialOffer'),
    path('print-technicalOffer/<str:offer_pk>/', views.print_technicalOffer, name='print-technicalOffer'),


    path('cancel-confirmedOrder/<str:pk>', views.cancel_confirmedOrder, name='cancel-confirmedOrder'),
    path('confirme-order/<str:pk>', views.confirm_order, name='confirm-order'),
    path('print-confirmedOrder/<str:offer_pk>/', views.print_confirmOrder, name='print-confirmedOrder'),

]

