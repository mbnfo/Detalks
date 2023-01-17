from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('login', views.login, name='login'),
    path('settings', views.settings, name='settings'),
    path('settings_signin', views.settings_signin, name='settings_signin'),
    path('checkview', views.checkview, name='checkview'),
    path('<str:room>/', views.room, name='room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('create_room', views.create_room, name = 'create_room'),
    path('addoption', views.addoption, name='addoption'),
    path('describer', views.describer, name= 'describer'),
    #path('vote_count', views.vote_count, name='vote_count')
]
