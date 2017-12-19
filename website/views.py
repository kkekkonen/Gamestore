from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

from django.db import models
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from website.models import *

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
    context = {}
    context["username"] = username
    context["permissions"] = permissions
    return render(request, 'homepage.html', context)
