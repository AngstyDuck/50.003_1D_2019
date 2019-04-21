from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('log_out/', views.log_out, name='logout'),
    path('reset_password/', views.reset_password, name='resetpassword'),
]
