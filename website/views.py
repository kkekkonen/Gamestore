from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.db import models
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
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
    context = {}
    context["games"] = games
    context["username"] = username
    context["permissions"] = permissions
    return render(request, 'homepage.html', context)

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
