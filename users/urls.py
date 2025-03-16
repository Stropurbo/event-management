from django.urls import path
from users.views import Signup,login_view,logout_view,activate_user,admin_dashboard,assign_role,create_group,group_list,no_permission

urlpatterns = [
    path('signup/', Signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign_role/', assign_role, name='assign_role'),
    path('admin/create_group/', create_group, name='create_group'),
    path('admin/group_list/', group_list, name='group_list'),
    path('no_permission/', no_permission, name='no_permission')
]
