from django.urls import path
from .views import views

app_name = "accounts"

urlpatterns = [
        path('signin/', views.signin, name='signin'),
        path('signup/', views.signup, name='signup'),
        path('profile/<str:user_name>', views.profile, name='profile'),
        path('edit/', views.edit, name='edit'),
        path('logout/', views.out, name='out'),
        path('rank/<str:token>', views.rank, name='rank'),
        path('connections/connect/discord', views.connection.connect, name='connections-connect-discord'),
        path('connections/connect/discord/authorize', views.connection.authorize, name='connections-connect-discord-authorize'),
        path('connections/disconnect/discord', views.connection.disconnect, name='connections-disconnect-discord'),
        path('delete_account/', views.delete_account, name='delete_account'),
]
