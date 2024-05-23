from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('project.urls')),
    path('', include('order.urls')),
    path('', include('quoteRequest.urls')),
    path('', include('commercialOffer.urls')),
    path('', include('invoice.urls')),
    path('', include('commission.urls')),
    path('', include('search_engine.urls')),
    path('i18n/', include('django.conf.urls.i18n')),

]
