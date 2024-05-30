from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.project_home,name='project-home'),
    path('create-project',views.project_create,name='create-project'),
    path('get-project/<str:project_nbr>',views.project_detail,name='project-detail'),
    path('update-project/<str:pk>',views.project_edit,name='update-project'),
    path('delete-project/<str:pk>',views.project_delete,name='delete-project'),
    path('add-article-to-project',views.add_article_to_project ,name='add-article-to-project'),
    path('remove-article-from-project/<str:project_pk>/<str:article_pk>',views.remove_article_from_project,name='remove-article-from-project'),
    path('get-projectsByKeyWord',views.get_projectsByKeyWord,name='get-projectsByKeyWord'),

    path('upload-file-to-project/<str:project_pk>',views.upload_file_to_project,name='upload-file-to-project'),
    path('download-file/<str:file_pk>',views.download_file,name='download-file'),
    path('remove-file/<str:file_pk>',views.remove_file,name='remove-file'),


    path('create-client',views.client_create,name='create-client'),
    path('update-client/<str:pk>',views.client_edit,name='update-client'),
    path('get-clientByRef/<str:ref>',views.get_clientByRef,name='get-clientByRef'),
    path('get-clientByKeyWord',views.get_clientsByKeyWord,name='get-clientByKeyWord'),

    
    path('create-supplier',views.supplier_create,name='create-supplier'),
    path('update-supplier/<str:pk>',views.update_supplier,name='update-supplier'),
    path('get-supplierByKeyWord/', views.get_suppliersByKeyWord, name='get-supplierByKeyWord'),
    path('get-supplierDetailByKeyWord/', views.get_supplierDetailByKeyWord, name='get-supplierDetailByKeyWord'),


    path('create-buyer',views.create_buyer,name='create-buyer'),
    path('get-buyersByKeyWord',views.get_buyersByKeyWord,name='get-buyersByKeyWord'),
    path('chose-buyer/',views.chose_buyer,name='chose-buyer'),
]

