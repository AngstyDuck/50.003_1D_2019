from django.urls import path

from . import views

app_name = 'createuser'
urlpatterns = [
    path('', views.get_user, name='index'),
]
