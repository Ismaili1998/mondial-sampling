from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.project_home,name='project-home'),
    path('create_project',views.project_create,name='create-project'),
    path('update_project',views.project_edit,name='update-project'),
    path('delete_project',views.project_delete,name='delete-project'),
    path('get_projectsByKeyWord',views.get_projectsByKeyWord,name='get-projectsByKeyWord'),

]

