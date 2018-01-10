from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.urls import reverse

from django.db import models
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from website.models import *
from website.forms import *

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
            return render(request, 'registration/auth_error.html')

#@permission_required('website.developer_rigths')
@login_required
def settings(request):
    return render(request, 'registration/settings.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def my_games(request):
    pass

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
