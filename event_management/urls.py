from django.contrib import admin
from django.urls import path,include
from users.views import login_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),   
    path('users/', include('users.urls')),   
    path('', login_view, name='login'),  
]
