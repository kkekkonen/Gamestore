from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.db import models
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from website.models import *
from website.forms import *

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
    data = {"name":name, "url":url, "description":description}
    form = GameForm(data)
    if form.is_valid():
        game_data = {
            'name': form.cleaned_data['name'],
            'url': form.cleaned_data['url'],
            'description': form.cleaned_data['description'],
            'owner':request.user,
        }
        game = Game(**game_data)
        game.save()
        return redirect('home')
    else:
        return HttpResponse(status=204)
