from django.urls import path
from . import views

app_name = "resources"

urlpatterns = [
        path('', views.resources, name='resources'),
        path('42ctf', views.ctf42, name='42ctf'),
        path('tools', views.tools, name='tools'),
        path('create_challenge', views.create_challenge, name='create_challenge'),
        path('translate', views.translate, name='translate'),
        path('edit', views.edit, name='edit'),
        path('donate', views.donate, name='donate'),
]
