from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Team, UserPlayer, Point
from .forms import UserPlayerForm, TeamForm, PointForm
from django.utils import timezone

import pdb

class IndexView(generic.ListView):
	template_name = 'teams/index.html'
	context_object_name = 'teams_list'
	
	def get_queryset(self):
		"""Return all teams"""
		return Team.objects.all().order_by('-created_date')

class TeamView(generic.DetailView):
	model = Team
	template_name = 'teams/detail.html'

@login_required
def players(request, team_id, player_id):
	player = get_object_or_404(UserPlayer, pk=player_id)
	team = get_object_or_404(Team, pk=team_id)
	form_class = PointForm
	
	if request.method == "POST":
		form = form_class(request.POST, request.FILES)
		
		if form.is_valid():
			point = form.save(commit=False)
			point.player = player
			point.point_owner = request.user
			point.save()
			player.points_scored += point.point
			player.save()
		else:
			return render(request, 'players/idex.html', {
				'player': player,
				'team': team,
				'points': Point.objects.filter(player=player),
				'form': form_class,
				'error_message': "Note is required",
			})
			
	context = {
		'player': player,
		'team': team,
		'points': Point.objects.filter(player=player),
		'form': form_class,
	}
	return render(request, 'players/index.html', context)

@login_required
def create_player(request, team_id):
	team = get_object_or_404(Team, pk=team_id)
	form_class = UserPlayerForm

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)

		if form.is_valid():
			new_player = form.save(commit=False)
			new_player.player_team = team
			new_player.save()
			return HttpResponseRedirect(reverse('cloud_roni:team', args= (team.id,)))
		else:
			return render(request, 'players/create.html', {
					'form': form_class,
					'team': team,
					'error_message': "Invalid Information!",
				})

	return render(request, 'players/create.html', {
				'form': form_class,
				'team': team,
				})

@login_required
def create_team(request):
	form_class = TeamForm

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)

		if form.is_valid():
			new_team = form.save(commit=False)
			new_team.created_date = timezone.now()
			new_team = form.save()
			return HttpResponseRedirect(reverse('cloud_roni:index'))
		else:
			return render(request, 'teams/create.html', {
					'form': form_class,
					'error_message': "Invalid Information!",
				})

	return render(request, 'teams/create.html', {
				'form': form_class,
				})