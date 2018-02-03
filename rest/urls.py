from django.urls import include, path
import rest.views as rest_views
from django.http import JsonResponse

urlpatterns = [
    path('rest/games', rest_views.all_games, name='rest_games'),
    path('rest/login', rest_views.rest_login, name='rest_login'),
    path('rest/logout', rest_views.rest_logout, name='rest_logout'),
    path('rest/mygames', rest_views.user_games, name='user_games'),
]
