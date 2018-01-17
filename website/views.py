from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.db import models
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from website.models import *
from website.forms import *
from hashlib import md5
from datetime import datetime

def is_developer(user):
    return user.has_perm('website.developer_rights')

def give_dev_rights(user):
    permission = Permission.objects.get(codename="developer_rights")
    user.user_permissions.add(permission)

#@permission_required('website.developer_rigths')
@login_required
def home(request):

    if not is_developer(request.user):
        give_dev_rights(request.user)

    username = request.user.username
    permissions = Permission.objects.filter(user=request.user)
    games = Game.objects.all()
    form = GameForm()
    context = {}
    context["games"] = games
    context["username"] = username
    context["permissions"] = permissions
    context["form"] = form
    return render(request, 'homepage.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_game(request):
    name = request.POST.get('name')
    url = request.POST.get('url')
    description = request.POST.get('description')
    price = request.POST.get('price')
    data = {"name":name, "url":url, "description":description, "price":price}
    form = GameForm(data)
    if form.is_valid():
        game_data = {
            'name': form.cleaned_data['name'],
            'url': form.cleaned_data['url'],
            'description': form.cleaned_data['description'],
            'price':form.cleaned_data['price'],
            'owner':request.user,
        }
        game = Game(**game_data)
        game.save()
        return redirect('home')
    else:
        print(form.errors)
        return HttpResponse(status=204)
def make_checksum(pid, sid, amount, secret_key):
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return checksum

def game_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    user_games = get_games(request.user)
    context = {}
    context["game"] = game
    if game not in user_games:
        pid = "game" + str(game_id) + request.user.username
        sid = "IHaveSpentTooMuchTimeOnThisIDWSD20172018"
        secret_key = "aa3dfa29c26efc70b4795f4cfb078f20"
        checksum = make_checksum(pid, sid, game.price, secret_key)
        context["amount"] = game.price
        context["owned"] = False
        context["pid"] = pid
        context["sid"] = sid
        context["success_url"] = "http://localhost:8000/games/" + str(game_id) + "/buy"
        context["checksum"]  = checksum
    else:
        context["owned"] = True
    return render(request, 'game.html', context)

def get_games(user):
    purchases = Purchase.objects.filter(user = user)
    games = []
    for purchase in purchases:
        games.append(purchase.game)
    return games
def game_buy(request, game_id):
    if request.method == "GET":
        pid = request.GET["pid"]
        ref = request.GET["ref"]
        result = request.GET["result"]
        checksum = request.GET["checksum"]
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, "aa3dfa29c26efc70b4795f4cfb078f20")
        checksum_test = md5(checksumstr.encode("ascii")).hexdigest()
        if result == "success" and checksum == checksum_test:
            game = Game.objects.get(pk=game_id)
            if game not in get_games(request.user):
                pass
                Purchase.objects.create(game=game, user=request.user, timestamp=datetime.now())
            url = "http://localhost:8000/games/" + str(game_id)
            return redirect(url)
        elif result == "cancel" and checksum == checksum_test:
            #throw cancel page
            pass
        elif result == "error":
            #throw error page
            pass
        else:
            url = "http://localhost:8000/games/" + str(game_id)
            return redirect(url)
