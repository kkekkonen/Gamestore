from django.shortcuts import render
from django.core import serializers
from website.models import Game, Score, Purchase
from rest.models import ApiKey
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotModified
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from itertools import chain

# Create your views here.

def check_token(request):
    body_token = json.loads(request.body)['token']
    db_token = ApiKey.objects.get(user=request.user).token
    return db_token == body_token

def all_games(request):
    if request.method == 'GET':
        data = serializers.serialize('python', Game.objects.all(), fields=('name', 'url', 'description', 'price'))
        all_games = [d['fields'] for d in data]
        return JsonResponse(all_games, safe=False)
    else:
        raise Http404

def user_games(request):
    if request.method == 'GET' and check_token(request):
        purchase_list = list(Purchase.objects.filter(user=request.user).values_list('game', flat=True))
        game_list = Game.objects.filter(id__in=purchase_list)

        data = serializers.serialize('python', game_list, fields=('name', 'url', 'description', 'price'))
        all_games = [d['fields'] for d in data]
        return JsonResponse(all_games, safe=False)
    else:
        raise Http404

def rest_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return HttpResponse(status=200)
    else:
        raise Http404

def rest_login(request):
    if request.method == 'GET' and not request.user.is_authenticated:
        username = request.GET.get('username')
        raw_password = request.GET.get('password')
        user = auth_authenticate(request, username=username, password=raw_password)
        if user is not None:
            try:
                rest_token = ApiKey.objects.get(user=user).token
            except:
                apikey_entry = ApiKey()
                apikey_entry.user = User.objects.get(username=username)
                apikey_entry.save()
                rest_token = apikey_entry.token
            
            auth_login(request, user)
            ret = {
                'token': rest_token
            }
            return JsonResponse(ret)
        else:
            raise Http404
    else:
        raise Http404