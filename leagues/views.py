# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseNotFound
from leagues.forms import LeagueForm
from leagues.models import League, Winner, Season
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from CloudRoni.models import Team
from cloud_project.settings import TIME_ZONE
import dateutil.parser
import datetime
import pytz

import pdb

# Create your views here.
@csrf_exempt
def start_new_season(request):
	end_date = dateutil.parser.parse(request.POST.get('date'))
	end_date = pytz.timezone(TIME_ZONE).localize(end_date, is_dst=None)
	if end_date.date() < datetime.date.today() or end_date.date() < datetime.date.today() + datetime.timedelta(weeks=1):
		response = HttpResponse('Invalid Date - Select a date one week or more in the future')
		response.status_code = 500
		return response
	else:
		league = request.user.league
		league.end_date = end_date
		league.ended = False
		league.save()
		return JsonResponse({'url': reverse('cloud_roni:index')})

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

def terminate_season(request):
	league = request.user.league
	if Team.objects.filter(league=league).count() < 3:
		form = LeagueForm(request.POST or None, instance=request.user.league)
		return render(request, 'leagues/league_management.html', {'form': form, 'confirmation': 'League is too small to terminate :('})
	end_season(league)
	return HttpResponseRedirect(reverse('cloud_roni:index'))

def end_season(league):
	teams =  Team.objects.filter(league=league).order_by('-team_points').reverse()[:3]
	winner_dict = {}
	for idx, team in enumerate(teams):
		winner = Winner(individual=str(team.team_owner),
						team_name=str(team.team_name),
						total_points=team.team_points)
		winner.save()
		winner_dict[idx] = winner
		team.delete()

	season = Season(league=league,
					first=winner_dict[0],
					second=winner_dict[1],
					third=winner_dict[2])
	season.save()

	league.ended = True
	league.end_date = None
	league.save()