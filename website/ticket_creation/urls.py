from django.urls import path

from . import views

app_name = 'ticket_creation'
urlpatterns = [
    path('', views.create, name='create'),
    path('display/', views.list, name='display'),
    path('delete/', views.delete, name='delete'),
    path('detail/', views.detail, name='detail'),
    path('resolve/', views.resolve, name='resolve'),
    path('selected_list/', views.selected_list, name='selected_list'),
    path('viewUnread/', views.viewUnread, name='unread'),
    path('viewUnresolve/', views.viewUnresolved, name='unresolve'),
]
