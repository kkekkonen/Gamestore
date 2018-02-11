from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.urls import reverse

from django.db import models
from django.db.models import Q #ei vissii importtaa tol ylemmäl... -ei, enkä tiedä miks
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from website.models import *
from website.forms import *
from hashlib import md5
import json
import time
from datetime import datetime
from collections import defaultdict

def is_developer(user):
    return user.has_perm('website.developer_rights')

def give_dev_rights(user):
    permission = Permission.objects.get(codename="developer_rights")
    user.user_permissions.add(permission)

def handler404(request):
    return render('registration/auth_error.html')

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('home', )

def user_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = auth_authenticate(request, username=username, password=raw_password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('home'))
        else:
            context = {
                'message': 'Invalid login! Please try again.',
                'message_type': 'bg-danger',
            }
            return render(request, 'registration/auth_error.html', context)

#@permission_required('website.developer_rigths')
@login_required
def settings(request):
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'account/settings.html', context)
    elif request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get('username'))
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.set_password(request.POST.get('password1'))
            user.save()
            context['message'] = 'Account settings changed successfully!'
            context['message_type'] = 'bg-success'
            return redirect(reverse('user_login'), context)
        except:
            context['message'] = 'Something went wrong! Please try again.'
            context['mesage_type'] = 'bg-danger'
            return render(request, 'account/settings.html', context)


def signup(request):
    error_context = {
        'message_type': 'bg-danger',
        'message': 'Invalid form! Please try again.'
    }
    if request.method == 'POST':
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth_authenticate(request, username=username, password=raw_password)
            auth_login(request, user)
            return redirect(reverse('home'))
        else:
            return render(request, 'registration/signup.html', error_context)
    elif request.method == 'GET':
        return render(request, 'registration/signup.html')

def home(request):
    return render(request, 'home.html')

def my_games(request):
    pass

def verify_email(request):
    pass

@permission_required('website.developer_rigths')
@login_required
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
        return redirect('dev_games')
    else:
        return dev_games(request, True, "failed to add game", "danger")

def make_checksum(pid, sid, amount, secret_key):
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return checksum

@login_required
def game_view(request, game_id, display=False, message="", color=""):
    game = get_object_or_404(Game, pk=game_id)
    user_games = get_games(request.user)
    context = {}
    context["game"] = game
    context["display"] = display
    context["result_message"] = message
    context["color"] = color
    context["creator"] = False
    if request.user == game.owner:
        context["creator"] = True
    if game not in user_games and game.owner != request.user:
        pid = "game" + str(game_id) + request.user.username
        sid = "IHaveSpentTooMuchTimeOnThisIDWSD20172018"
        secret_key = "aa3dfa29c26efc70b4795f4cfb078f20"
        checksum = make_checksum(pid, sid, game.price, secret_key)
        context["amount"] = game.price
        context["owned"] = False
        context["pid"] = pid
        context["sid"] = sid
        context["checksum"]  = checksum
    else:
        context["owned"] = True
    return render(request, 'game.html', context)

def get_games(user):
    #function is used to collect a users owned games
    purchases = Purchase.objects.filter(user = user)
    games = []
    for purchase in purchases:
        games.append(purchase.game)
    return games

@login_required
def game_buy(request, game_id):
    #this function is used to process a purchase request. a purchase is successfull only if the
    #checksum is correct and result is "success". If purchase fails for any reason a error is displayed
    if request.method == "GET":
        pid_test = "game" + str(game_id) + request.user.username
        pid = request.GET.get("pid", "")
        ref = request.GET.get("ref", "")
        result = request.GET.get("result", "")
        checksum = request.GET.get("checksum", "")
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, "aa3dfa29c26efc70b4795f4cfb078f20")
        checksum_test = md5(checksumstr.encode("ascii")).hexdigest()
        if result == "success" and checksum == checksum_test and pid == pid_test:
            game = Game.objects.get(pk=game_id)
            if game not in get_games(request.user):
                Purchase.objects.create(game=game, user=request.user, timestamp=datetime.now())
            return game_view(request, game_id, True, "Purchase successful", "success")
        elif result == "cancel" and checksum == checksum_test and pid == pid_test:
            return game_view(request, game_id, True, "Purchase canceled", "warning")
        elif result == "error":
            return game_view(request, game_id, True, "Failed to purchase game", "danger")
        else:
            return game_view(request, game_id, True, "parameter missing or invalid", "danger")

@login_required
def save_score(request, game, score):
    #this function is used to save a score. Used in function game_request below
    #a score is only saved if it is better than the users old score in the same game.
    try:
        score_int = int(score)
        old_score = Score.objects.get(game=game, user=request.user)
        if(int(score) > old_score.score):
            old_score.delete()
            Score.objects.create(game=game, user=request.user, score=score)
    except Score.DoesNotExist:
        Score.objects.create(game=game, user=request.user, score=score)

@login_required
def load_gameState(request, game):
    #this function tries to load the gamestate the user has previously saved. Used in function game_request below
    try:
        gamestate = GameState.objects.get(game=game, user=request.user).gamestate
    except GameState.DoesNotExist:
        return  {"messageType": "ERROR", "info": "Gamestate could not be loaded, you don't have any saves for this game!"}
    return json.loads(gamestate)

@login_required
def save_gameState(request, game, json_string):
    #this function saves the game when the users request's messagetype is "SAVE". Used in function game_request below
    #the service deletes old saves and saves the json the user has sent in the Purchase-model.
    try:
        old_gameState = GameState.objects.filter(user=request.user, game=game)
        old_gameState.delete()
    except GameState.DoesNotExist:
        pass
    GameState.objects.create(game=game, user=request.user, gamestate=json_string)
    return HttpResponse(status=204)


@login_required
def game_request(request, game_id):
    #function processes all the request made by the game/user to the service such as save/loads
    game = get_object_or_404(Game, pk=game_id)
    if(request.method == "POST"):
        json_string = request.read().decode('utf-8')
        messageType = json.loads(json_string).get('messageType')
        if messageType == "SAVE":
            save_gameState(request, game, json_string)
        elif messageType == "SCORE":
            save_score(request, game, json.loads(json_string).get("score"))
            return HttpResponse(status=204)
    else:
        messageType = request.GET.get("messageType")
        if messageType == "LOAD_REQUEST":
            data = load_gameState(request, game)
            data["messageType"] = "LOAD"
            return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(status=204)

def search(request):
    searchgame_list = Game.objects.all()
    searchtext = request.GET.get("q")

    if searchtext:
        searchgame_list = searchgame_list.filter(
            Q(name__icontains = searchtext)
            )

    context = {
        "games_list": searchgame_list,
    }
    
    if request.user.is_authenticated:
        user_games = get_games(request.user)
        context["user_games"] = user_games

    return render(request, 'search.html', context)

def categories(request):
    games_list = Game.objects.all()
    chosencategory = request.GET.get("cat")
    category = Category.objects.all()
    #if chosencategory:
    #    games_list = games_list.filter(
    #        Q(category__icontains = chosencategory)
    #        )
    context = {
        "games_list": games_list,
        "categorys_list":category,
        "chosencategory": chosencategory,
    }

    if request.user.is_authenticated:
        user_games = get_games(request.user)
        context["user_games"] = user_games

    return render(request, 'categories.html', context)

@login_required
@permission_required('website.developer_rigths')
def dev_games(request, display=False, message="", color=""):
    #function collects the games the user-developer has made to populate the dev_edit templates edit-forms
    games = Game.objects.filter(owner=request.user).all()
    context = {}
    context["display"] = display
    context["result_message"] = message
    context["color"] = color
    context["games"] = games
    return render(request, 'dev_edit.html', context)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required
@permission_required('website.developer_rigths')
def edit_game(request):
    #function is used by developers to edit pre-existing games in "dev_edit" template
    game_id = request.POST.get("id")
    game = get_object_or_404(Game, pk=game_id)
    #check that the user owns the game he is about to edit
    if(request.user == game.owner):
        validate = URLValidator()
        display = False
        message = ""
        name = request.POST.get("name")
        url = request.POST.get("url")
        description = request.POST.get("description")
        price = request.POST.get("price")
        if name:
            game.name=name
        if url:
            try:
                validate(url)
                game.url=url
            except ValidationError:
                display =True
                message += "Url is invalid"
        if description:
            game.description=description
        if price and is_int(price):
            game.price=price
        game.save()
        return dev_games(request, display, message, "warning")
    return dev_games(request, True, "Failed to edit the game", "danger")
'''
@login_required
@permission_required('website.developer_rigths')
def game_stats(request, game_id):
    #this function is used to create the data required in a selling statistic-graph
    your_games = Game.objects.filter(owner=request.user).all()
    result = {}
    for game in your_games:
        #time.mktime(x.timestamp.timetuple())
        result[game.id] = (list(map(lambda x: x.timestamp, Purchase.objects.filter(game=game).all())))
    print(result)
'''

@login_required
@permission_required('website.developer_rigths')
def game_stats(request, game_id):
    #this function is used to create a json used to display selling data of a game
    game = Game.objects.get(pk=game_id)
    if(game.owner == request.user):
        purchases = (list(map(lambda x: x.timestamp, Purchase.objects.filter(game=game).all())))
        purchases.sort()
        dates = defaultdict(lambda:defaultdict(int))
        now = datetime.now()
        for i in range(1, 13):
            if( i > now.month):
                dates[now.year-1][i] = 0
            if i <= now.month :
                dates[now.year][i] = 0
        for purchase in purchases:
            year = purchase.year
            month = purchase.month
            dates[year][month] += 1
        return HttpResponse(json.dumps(dates), content_type='application/json')
    else:
        return HttpResponse(status=403)
