"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from createuser.views import get_user
from ticket_creation.views import create, list,delete


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('home/', include('home.urls'), name='home'),
    path('', include('login.urls'), name='login'),
    path('createuser/', include('createuser.urls'), name='createuser'),
    path('ticket_creation/', include('ticket_creation.urls'), name='ticket_creation'),
    path('Profile/', include('Profile.urls'), name='Profile'),
]
