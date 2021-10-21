"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns

from django.views import defaults
from django.contrib import admin
from django.urls import include, re_path, path
import home

urlpatterns = [
    path('', include('home.urls')),
    path('set_lang/<str:lang_code>', home.views.set_language, name="set_language"),
    path('dashboard/secret/admin', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('ctfs/', include('ctfs.urls')),
    re_path('^accounts/login/', defaults.page_not_found, {'exception': Exception()}),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('scoreboard/', include('scoreboard.urls')),
    path('events/', include('events.urls'))
)
