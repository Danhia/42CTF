from django.urls import path
from . import views

urlpatterns = [
        path('<str:cat_slug>/', views.category, name='category'),
        path('<str:cat_slug>/<str:ctf_slug>', views.ctf, name='ctf')
]
