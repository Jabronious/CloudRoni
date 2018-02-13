# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseNotFound
from leagues.forms import LeagueForm
from leagues.models import League
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import pdb

# Create your views here.
def create_league(request):
	form_class = LeagueForm

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)

		if form.is_valid():
			try:
				League.objects.get(owner=request.user)
				return render(request, 'leagues/create.html', {
					'form': form_class,
					'error_message': "You have already created a league.",
				})
			except:
				form.cleaned_data['end_date']
				new_league = form.save(commit=False)
				new_league.created_date = timezone.now()
				new_league.owner = request.user
				new_league.save()
				new_league.participants.add(request.user)
				new_league.save()
				return HttpResponseRedirect(reverse('cloud_roni:index'))
		else:
			return render(request, 'leagues/create.html', {
					'form': form_class,
					'error_message': "Invalid Information!",
				})

	return render(request, 'leagues/create.html', {'form': form_class,})

class LeaguesListView(generic.ListView):
	template_name = 'leagues/join.html'
	context_object_name = 'leagues_list'

	def get_queryset(self):
		"""Return all teams ordered by team_points"""
		return League.objects.all().order_by('-created_date')

@csrf_exempt
def join_league(request):
	league_code = request.POST.get('code')
	league = League.objects.get(pk=int(request.POST.get('league_id')))
	if league.signup_code == league_code:
		league.participants.add(request.user)
		league.save()
		return JsonResponse({'url': reverse('cloud_roni:index')})
	else:
		return HttpResponseNotFound('Incorrect League Code')

def home_page(request):
	if request.user.is_authenticated():
		try:
			League.objects.get(participants=request.user)
			return HttpResponseRedirect(reverse('cloud_roni:index'))
		except:
			return HttpResponseRedirect(reverse('leagues:leagues_index'))

	register_form_class = UserCreationForm
	
	return render(request, 'leagues/home_page.html', {'form': register_form_class,})

@login_required
def manage_league(request):
	form = LeagueForm(request.POST or None, instance=request.user.league)
	confirmation = ''

	if request.method == "POST" and form.is_valid():
		confirmation = 'Updated League!'
		form.cleaned_data['end_date']
		form.save()

	return render(request, 'leagues/league_management.html', {'form': form, 'confirmation': confirmation})