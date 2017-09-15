# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('cloud_roni:index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('cloud_roni:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def update_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated() and request.user.id == user.id:
        form = UserUpdateForm(request.POST or None, instance=user)
    
        context = {
            'user': user,
            'form': form,
        }
    
        if form.is_valid():
            form.save()
    
        return render(request, 'users/account.html', context)
    else:
        raise PermissionDenied