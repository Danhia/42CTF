from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
        path('', views.events, name='events'),
        path('<str:event_slug>', views.event, name='event_info'),
        path('<str:event_slug>/challenge/<str:chall_slug>', views.chall_event_info, name='event_chall_info'),
        path('pwd/<str:event_slug>', views.submit_pwd, name='submit_pwd'),
        path('submitEventFlag/<str:event_slug>/<str:chall_slug>', views.submit_event_flag, name='submit_event_flag'),
        path('register/<str:event_slug>', views.register_to_event, name='register_event'),
        path('create_team/<str:event_slug>', views.create_team, name='create_team'),
        path('join_team/<str:event_slug>', views.join_team, name='join_team'),
        path('<str:event_slug>/profile/<str:user_name>', views.profile, name='profile'),
        path('<str:event_slug>/team/<str:name>', views.team_info, name='team_info'),
        path('<str:event_slug>/manage_team', views.manage_team, name='manage_team'),
        path('<str:event_slug>/leave_team', views.leave_team, name='leave_team'),
        path('find_team/<str:event_slug>', views.find_team, name='find_team'),
        path('<str:event_slug>/open_team', views.open_team, name='open_team'),
        path('<str:event_slug>/close_team', views.close_team, name='close_team'),
]
