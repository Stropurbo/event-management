from django.contrib import admin
from django.urls import path,include
# from users.views import login_view
from tasks.views import home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),   
    path('users/', include('users.urls')),   
    # path('login', login_view, name='login'),  
    path('', home, name='home'),  
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)