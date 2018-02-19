from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.urls import reverse
from django.forms.utils import ErrorList
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from website.models import *
from website.forms import *
from hashlib import md5
import json
import time
from datetime import datetime
from collections import defaultdict
#these imports are used by email verification (activate, signup, send_activation_email)
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
#email verification imports end
import os
from urllib.request import urlopen
from collections import Counter

SELLER_ID = 'IHaveSpentTooMuchTimeOnThisIDWSD20172018'
PAYMENT_SECRET_KEY = 'aa3dfa29c26efc70b4795f4cfb078f20'

def give_dev_rights(user):
    #this function is used to give a user the developer-permission
    permission = Permission.objects.get(codename="developer_rights")
    user.user_permissions.add(permission)

@login_required
def request_developer_permissions(request):
    give_dev_rights(request.user)
    return redirect('settings')


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

def send_activation_email(request, user, email):
    #this is a function used to send a account activation email usind django console backend
    subject = 'Activate your account'
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.id)).decode()
    token = account_activation_token.make_token(user)
    sender = 'admin@gmail.com'
    msc = 'use this link to activate your account:\n'
    email = EmailMessage(subject, msc + domain + '/activate/' + str(uid)  + '/' + token, sender, [email])
    email.send(fail_silently=False)

def activate(request, uid, token):
    #function used to activate a new account.
    try:
        uid_byte = uid.encode()
        user_id = force_text(urlsafe_base64_decode(uid_byte))
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('user_login')
    else:
        context = {'result_message': 'Invalid activation link!', 'color': 'danger', 'display': True}
        return render(request, 'homepage.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.is_active = False
            user.save()
            #send the activation email
            send_activation_email(request, user, form.cleaned_data.get('email'))
            #if the user checked the developer checkbox, grant him dev permission
            if(request.POST.get('developer') == 'on'):
                give_dev_rights(user)
            context = {}
            context['token'] = account_activation_token.make_token(user)
            context['uid'] = urlsafe_base64_encode(force_bytes(user.id)).decode()
            context['domain'] = get_current_site(request).domain
            context['username'] = username
            return render(request, 'activation_email.html', context)
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

def home(request):
    #the function for home view. Gets the 5 most sold games of all time and lists them
    games = Counter((list(map(lambda x: x.game, Purchase.objects.all()))))
    popular_games= [game for game, game_count in Counter(games).most_common(3)]
    return render(request, 'home.html', {"games": popular_games})

def check_image_url(url):
    #this function is used to check if a url can be used to load a image
    try:
        #check that the url works
        urlopen(url)
        #check that the file url leads to image
        if any([url.endswith(e) for e in [".jpg", ".jpeg", ".png", ".gif", "svg"]]):
            return True
    except Exception as e:
        pass
    return False

@permission_required('website.developer_rights')
@login_required
def add_game(request):
    #function used to add a new game to the service. user must be logged in and
    # have permission to add Games
    # uses GameForm to render the form.
    if(request.method == "POST"):
        name = request.POST.get('name')
        url = request.POST.get('url')
        image_url = request.POST.get('image_url')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        data = {"name":name, "url":url, "image_url":image_url, "description":description, "price":price, "category":category}
        form = GameForm(data)
        if image_url != "" and not check_image_url(image_url):
            form.add_error("image_url", "invalid image url")
        if form.is_valid():
            game_data = {
                'name': form.cleaned_data['name'],
                'url': form.cleaned_data['url'],
                'image_url': form.cleaned_data['image_url'],
                'description': form.cleaned_data['description'],
                'price':form.cleaned_data['price'],
                "category":form.cleaned_data['category'],
                'owner':request.user,
            }
            game = Game(**game_data)
            game.save()
            return redirect('edit_game', game_id=game.id)
        else:
            context = {}
            context["form"] = form
            return render(request, 'add_game.html', context)
    else:
        return render(request, 'add_game.html', {"form": GameForm()})


def make_checksum(pid, sid, amount, secret_key):
    #function used to make the checksum used when buying the game
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return checksum

@login_required
def game_view(request, game_id, display=False, message="", color=""):
    #function used when rendering the gameview.
    #if the user owns/has purchased the game, he sees the game and top score.
    #owner also sees the selling statistics.
    #otherwise the user has the option to purchase the game
    game = get_object_or_404(Game, pk=game_id)
    user_games = get_games(request.user)
    context = {}
    context["url"] = get_current_site(request).domain + "/games/" + str(game_id)
    context["game"] = game
    context["display"] = display
    context["result_message"] = message
    context["color"] = color
    context["creator"] = False
    if request.user == game.owner:
        context["creator"] = True
    if game not in user_games and game.owner != request.user:
        pid = "game" + str(game_id) + request.user.username
        sid = SELLER_ID
        secret_key = PAYMENT_SECRET_KEY
        checksum = make_checksum(pid, sid, game.price, secret_key)
        context["amount"] = game.price
        context["owned"] = False
        context["pid"] = pid
        context["sid"] = sid
        context["checksum"]  = checksum
    else:
        #populate the score list. Scores are not visible if there are no scores for the game
        context["scores"] = Score.objects.filter(game=game).order_by('-score')[:5]
        context["owned"] = True
    return render(request, 'game.html', context)

def get_games(user):
    #function is used to collect a users owned games
    purchases = Purchase.objects.filter(user = user)
    games = []
    for purchase in purchases:
        games.append(purchase.game)
    created_games = Game.objects.filter(owner = user).all()
    return list(created_games) + games

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
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid_test, ref, result, PAYMENT_SECRET_KEY)
        checksum_test = md5(checksumstr.encode("ascii")).hexdigest()
        if result == "success" and checksum == checksum_test and pid == pid_test:
            game = get_object_or_404(Game, pk=game_id)
            if game not in get_games(request.user):
                Purchase.objects.create(game=game, user=request.user, timestamp=datetime.now())
            else:
                #you already have the game
                return redirect('game_view', game_id=game_id)
            return game_view(request, game_id, True, "Purchase successfull", "success")
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
    except ValueError:
        #the score was not Int.
        pass

@login_required
def load_gameState(request, game):
    #this function tries to load the gamestate the user has previously saved. Used in function game_request below
    try:
        gamestate = eval(GameState.objects.get(game=game, user=request.user).gamestate)
        gamestate["messageType"] = "LOAD"
    except GameState.DoesNotExist:
        return  {"messageType": "ERROR", "info": "Gamestate could not be loaded, you don't have any saves for this game!"}
    return gamestate

@login_required
def save_gameState(request, game, json_string):
    #this function saves the game when the users request's messagetype is "SAVE". Used in function game_request below
    #the service deletes old saves and saves the json the user has sent in the Purchase-model.
    try:
        #only 1 gamestate is saved for a user per game.
        #delete the users old gamestates for the game.
        old_gameState = GameState.objects.filter(user=request.user, game=game)
        old_gameState.delete()
    except GameState.DoesNotExist:
        pass
    GameState.objects.create(game=game, user=request.user, gamestate=json_string)


@login_required
def game_request(request, game_id):
    #function processes all the request made by the game/user to the service such as save/loads
    game = get_object_or_404(Game, pk=game_id)
    if(request.method == "POST"):
        #the request is a POST-request. User is trying to save a Score/Gamestate
        json_string = request.read().decode('utf-8')
        messageType = json.loads(json_string).get('messageType')
        if messageType == "SAVE":
            save_gameState(request, game, json_string)
            return HttpResponse(status=204)
        elif messageType == "SCORE":
            save_score(request, game, json.loads(json_string).get("score"))
            return HttpResponse(status=204)
    else:
        #the request should be a LOAD_REQUEST (GET).
        messageType = request.GET.get("messageType")
        if messageType == "LOAD_REQUEST":
            data = load_gameState(request, game)
            return HttpResponse(json.dumps(data), content_type='application/json')
    raise Http404("invalid game request")

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
    context["search"] = searchtext
    return render(request, 'search.html', context)

def categories(request):
    games_list = Game.objects.all()
    chosencategory = request.GET.get("cat")
    categorychoices = CATEGORY_CHOICES
    if chosencategory:
        if len(chosencategory) > 0:
            games_list = games_list.filter(
                Q(category__icontains = chosencategory)
                )
    context = {
        "games_list": games_list,
        "chosencategory": chosencategory,
        "categorychoices": categorychoices,
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
@permission_required('website.developer_rights')
def edit_game(request, game_id):
    #function is used by developers to edit pre-existing games in "game_form" template
    game = get_object_or_404(Game, pk=game_id)
    #check that the user owns the game he is about to edit
    if(request.user == game.owner):
        if(request.method == "POST"):
            #if the user sent the form, process the data
            name = request.POST.get("name")
            url = request.POST.get("url")
            description = request.POST.get("description")
            price = request.POST.get("price")
            image_url = request.POST.get("image_url")
            category = request.POST.get('category')
            data = {"name":name, "url":url, "image_url":image_url, "description":description, "price":price, "category":category}
            form = GameForm(data)
            if image_url != "" and not check_image_url(image_url):
                form.add_error("image_url", "invalid image url")
            if form.is_valid():
                game.name = form.cleaned_data['name']
                game.url = form.cleaned_data['url']
                game.image_url = form.cleaned_data['image_url']
                game.description = form.cleaned_data['description']
                game.price = form.cleaned_data['price']
                game.category = form.cleaned_data['category']
                game.save()
            return render(request, 'edit_game.html', {"form": form, "game": game} )
        else:
            #if the user did not post the form, send form with the current values of the Game
            data = {"name":game.name, "url":game.url, "description":game.description, "price":game.price, "image_url":game.image_url, "category":game.category}
            form = GameForm(initial=data)
            return render(request, 'edit_game.html', {"form": form, "game": game} )
    raise Http404("invalid game edit request")

@login_required
@permission_required('website.developer_rights')
def game_stats(request, game_id):
    #this function is used to create a json used to display selling data of a game
    game = get_object_or_404(Game, pk=game_id)
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

@login_required
def my_games(request):
    #this function is used in my_games-page to populate the list of games
    context = {"games": get_games(request.user)}
    return render(request, 'my_games.html', context)

@login_required
@permission_required('website.developer_rights')
def delete_game(request, game_id):
    #function to delete a game which belongs to the user
    game = get_object_or_404(Game, pk=game_id)
    if(request.user == game.owner):
        game.delete()
        return redirect("my_games")
    else:
        return HttpResponse(status=403)
