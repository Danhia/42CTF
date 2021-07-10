from django.urls import path
from . import views

app_name = "scoreboard"

urlpatterns = [
        path('', views.scoreboard, name='scoreboard')
]
