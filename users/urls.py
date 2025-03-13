from django.urls import path
from users.views import Signup,login_view,logout_view

urlpatterns = [
    path('signup/', Signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', login_view, name='logout'),
]
