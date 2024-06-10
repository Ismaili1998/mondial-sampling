from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)