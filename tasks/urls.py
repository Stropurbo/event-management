from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from tasks.views import Home,CreateEvent,RSVP_EVENT,EventDetailsView,DashboardView,EventDetails,DeleteEvent,DeleteCategory,DeleteParticipant,CreateParticipant,CreateCategory,ShowCategory,UpdateEvent



urlpatterns = [
    # path('home/', home, name="home"),
    path('', Home.as_view(), name="home"),
    # path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    # path('create_event/', create_event, name= 'create_event'),
    path('create_event/', CreateEvent.as_view(), name= 'create_event'),
    path('update_event/<int:id>', UpdateEvent.as_view(), name='update_event'),
    # path('category_form/', create_category, name='category_form'),
    path('category_form/', CreateCategory.as_view(), name='category_form'),
    # path('participate_form/', create_participate, name='partici_form'),
    path('participate_form/', CreateParticipant.as_view(), name='partici_form'),
    # path('update_event/<int:id>', update_event, name='update_event'),
    # path('delete_event/<int:id>', delete_event, name='delete_event'),
    path('delete_event/<int:id>', DeleteEvent.as_view(), name='delete_event'),
    # path('delete_participant/<int:event_id>/<int:user_id>/', delete_participant, name='delete_participant'),
    path('delete_participant/<int:event_id>/<int:user_id>/', DeleteParticipant.as_view(), name='delete_participant'),
    # path('show_cat/', show_cat, name='show_cat'),
    path('show_cat/', ShowCategory.as_view(), name='show_cat'),
    # path('delete_cat/', delete_cat, name='delete_cat'),
    path('delete_cat/', DeleteCategory.as_view(), name='delete_cat'),
    # path('events/', event_details, name='event_details'),
    path('events/', EventDetails.as_view(), name='event_details'),
    # path('event<int:id>/event_detail/', event_details_view, name='event_details_view'),
    path('event<int:id>/event_detail/', EventDetailsView.as_view(), name='event_details_view'),
    # path('rsvp<int:event_id>/', rsvp_event, name='rsvp_event'),
    path('rsvp<int:event_id>/', RSVP_EVENT.as_view(), name='rsvp_event'),

] + debug_toolbar_urls()    
