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
#from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('add_game', views.add_game, name='add_game'),
    path('games/<int:game_id>', views.game_view, name='game_view'),
    path('games/<int:game_id>', views.game_view, name='game_view'),
    path('games/<int:game_id>/request', views.game_request, name='game_request'),
    path('games/<int:game_id>/buy', views.game_buy, name='game_buy')
]
