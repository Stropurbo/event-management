from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from tasks.views import home, create_event, create_category,delete_cat,delete_participant, show_cat,create_participate,update_event,dashboard,delete_event,event_details,event_details_view



urlpatterns = [
    path('home/', home, name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('create_event/', create_event, name= 'create_event'),
    path('category_form/', create_category, name='category_form'),
    path('participate_form/', create_participate, name='partici_form'),
    path('update_event/<int:id>', update_event, name='update_event'),
    path('delete_event/<int:id>', delete_event, name='delete_event'),
    path('delete_participant/<int:id>', delete_participant, name='delete_participant'),
    path('show_cat/', show_cat, name='show_cat'),
    path('delete_cat/', delete_cat, name='delete_cat'),
    path('events/', event_details, name='event_details'),
    path('event<int:id>/event_detail/', event_details_view, name='event_details_view'),
] + debug_toolbar_urls()    
