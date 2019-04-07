from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from . import views


app_name = 'vue_login'
urlpatterns = [
	path('admin/', admin.site.urls),
	path('login/', TemplateView.as_view(template_name='index.html')),
        path('test/', TemplateView.as_view(template_name='sample.html')),
	path('submit_login/', views.submit_login, name='submit_login'),
]
