from django.urls import path
from users.views import ActivateUser,UserDash,AdminEvent,GroupList,AssignRole,CreateGroup,AdminDashbaord,EditProfileView,SignupView,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView,no_permission
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('activate/<uidb64>/<token>/', ActivateUser.as_view(), name='activate_user'),


    path('admin/dashboard/', AdminDashbaord.as_view(), name='admin-dashboard'),
    path('admin/<int:user_id>/assign_role/', AssignRole.as_view(), name='assign_role'),
    path('admin/create_group/', CreateGroup.as_view(), name='create_group'),
    path('admin/group_list/', GroupList.as_view(), name='group_list'),
    path('no_permission/', no_permission, name='no_permission'),
    path('admin_event/', AdminEvent.as_view(), name='admin_event'),
    path('user_dashoard/', UserDash.as_view(), name='user_dash'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', ChangePassword.as_view(),name='change_password'),
    path('reset_password/', CustomPasswordResetView.as_view(),name='reset_password'),
    path('reset_password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('edit_profile/', EditProfileView.as_view(), name="edit_profile")


]
