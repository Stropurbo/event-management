from django.contrib import admin
from django.urls import path,include
from tasks.views import Home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),   
    path('users/', include('users.urls')),   
    path('', Home.as_view(), name='home'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)