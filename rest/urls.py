from django.urls import include, path
import rest.views as rest_views
from django.http import JsonResponse

urlpatterns = [
    path('rest/games', rest_views.all_games, name='rest_games'),
    path('rest/mygames', rest_views.user_games, name='user_games'),
    path('rest/highscores', rest_views.highscores, name='rest_highscores'),
    path('rest/sales', rest_views.all_sales, name='rest_sales'),
]
