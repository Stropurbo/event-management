from django.urls import path
from tasks.views import show_task,home

urlpatterns = [
    path('home/', home),
    path('show-task/', show_task),

]
