from django.shortcuts import render
from django.core import serializers
from website.models import Game, Score
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotModified
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def games(request):
    if request.method == 'GET':
        data = serializers.serialize('python', Game.objects.all(), fields=('name', 'url', 'description', 'price'))
        all_games = [d['fields'] for d in data]
        return JsonResponse(all_games, safe=False)
    else:
        raise Http404

@login_required
def rest_logout(request):
    auth_logout(request)
    return HttpResponse(status=200)

def rest_login(request):
    if request.method == 'GET' and not request.user.is_authenticated:
        username = request.GET.get('username')
        raw_password = request.GET.get('password')
        user = auth_authenticate(request, username=username, password=raw_password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse(status=200)
        else:
            raise Http404
    else:
        raise Http404