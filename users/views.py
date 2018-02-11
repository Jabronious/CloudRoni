# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from users.forms import PhoneNumberForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from users.models import PhoneNumber
from django.utils import timezone
from leagues.forms import LeagueForm

import pdb

def logout_view(request):
    logout(request)
    return render(request, 'leagues/home_page.html', {'form': UserCreationForm,})

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
            return HttpResponseRedirect(reverse('leagues:leagues_index'))

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

@login_required
def create_or_update_phone_number(request):
    form_class = PhoneNumberForm
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                old_number = PhoneNumber.objects.get(user=user)
                new_number = form['number'].value()
                old_number.number = str(new_number)
                old_number.twilio_formatted_number = format_twilio_number(str(new_number))
                old_number.created_date = timezone.now()
                old_number.is_valid_phone_number = old_number.is_valid_number()
                old_number.save()
            except PhoneNumber.DoesNotExist:
                phone_number = form.save(commit=False)
                phone_number.user = user
                phone_number.twilio_formatted_number = format_twilio_number(phone_number.number)
                phone_number.created_date = timezone.now()
                phone_number.is_valid_phone_number = phone_number.is_valid_number()
                phone_number.save()
        return render(request, 'users/account.html', {'user': user, 'form': UserUpdateForm(request.POST or None, instance=user),})

    context = {
		'form': form_class,
	}
    return render(request, 'phone_numbers/update_phone_number.html', context)

def format_twilio_number(number):
        return '+1' + number