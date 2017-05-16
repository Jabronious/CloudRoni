from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse

from .models import Team, UserPlayer
from .forms import UserPlayerForm

import pdb

def index(request):
    teams_list = Team.objects.order_by('-created_date')[:10]
    context = {
		'teams_list': teams_list,
	}
    return render(request, 'teams/index.html', context)

def team(request, team_id):
	team = get_object_or_404(Team, pk=team_id)
	return render(request, 'teams/detail.html', {'team': team}) 

def players(request, team_id, player_id):
	player = get_object_or_404(UserPlayer, pk=player_id)
	team = get_object_or_404(Team, pk=team_id)
	context = {
		'player': player,
		'team': team
	}
	return render(request, 'players/index.html', context)

def create_player(request, team_id):
	team = get_object_or_404(Team, pk=team_id)
	form_class = UserPlayerForm

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)

		if form.is_valid():
			new_player = form.save(commit=False)
			new_player.player_team = team
			new_player.save()
			return HttpResponseRedirect(reverse('team', args= (team.id,)))
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