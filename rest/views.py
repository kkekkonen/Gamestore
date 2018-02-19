from django.shortcuts import render
from django.core import serializers
from website.models import Game, Score, Purchase
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotModified
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from itertools import chain
from django.contrib.auth.decorators import permission_required

# Create your views here.
def all_games(request):
    #makes a json with a list of all the games with all their fields
    if request.method == 'GET':
        data = serializers.serialize('python', Game.objects.all(), fields=('name', 'url', 'image_url', 'description', 'price', 'category'))
        all_games = [d['fields'] for d in data]
        return JsonResponse(all_games, safe=False)
    else:
        raise Http404

@login_required
def user_games(request):
    #makes a json with a list of all the games the request sender has purchased with all their fields
    if request.method == 'GET':
        purchase_list = list(Purchase.objects.filter(user=request.user).values_list('game', flat=True))
        game_list = Game.objects.filter(id__in=purchase_list)

        data = serializers.serialize('python', game_list, fields=('name', 'url', 'image_url', 'description', 'price', 'category'))
        all_games = [d['fields'] for d in data]
        return JsonResponse(all_games, safe=False)
    else:
        raise Http404

def highscores(request):
    #makes a json with a list of all the high scores stored in the database
    if request.method == 'GET':
        data = serializers.serialize('python', Score.objects.all(), fields=('game', 'user', 'score'), use_natural_foreign_keys=True)
        all_scores = [d['fields'] for d in data]
        return JsonResponse(all_scores, safe=False)
    else:
        raise Http404


@login_required
@permission_required('website.developer_rights')
def all_sales(request):
    #makes a json with a list of all the purchase events of the request sender
    if request.method == 'GET':
        your_games = Game.objects.filter(owner=request.user).all()
        data = serializers.serialize('python', Purchase.objects.filter(game__in=your_games).all(), fields=('game', 'timestamp'), use_natural_foreign_keys=True)
        all_sales = [d['fields'] for d in data]
        return JsonResponse(all_sales, safe=False)
    else:
        raise Http404
