"""gamestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

handler404 = 'website.views.handler404'

urlpatterns = [
    path('', views.home, name='home'),
    path('account/mygames', views.my_games, name='my_games'),
    # path('account/verify/<slug:slug>', views.verify_email, name='verify_email'),
    path('account/settings', views.settings, name='settings'),
    path('account/login/', views.user_login, name='user_login'),
    path('account/signup/', views.signup, name='signup'),
    path('account/logout/', views.user_logout, name='user_logout'),
    path('account/add_game', views.add_game, name='add_game'),
    path('games/<int:game_id>', views.game_view, name='game_view'),
    path('games/<int:game_id>/request', views.game_request, name='game_request'),
    path('games/<int:game_id>/buy', views.game_buy, name='game_buy'),
    path('account/developer', views.dev_games, name='dev_games'),
    path('account/edit_game', views.edit_game, name='edit_game'),
    path('games/<int:game_id>/statistics', views.game_stats, name='game_stats'),
]
