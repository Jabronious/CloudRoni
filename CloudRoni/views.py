from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import loader, RequestContext
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Team, UserPlayer, Point, Trade
from .forms import UserPlayerForm, TeamForm, PointForm

import pdb

class IndexView(generic.ListView):
	template_name = 'teams/index.html'
	context_object_name = 'teams_list'

	def get_queryset(self):
		"""Return all teams"""
		return Team.objects.all().order_by('-created_date')

class PlayersView(generic.ListView):
	template_name = 'players/all_players.html'
	context_object_name = 'players_list'

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			result = UserPlayer.objects.filter(player_first_name=query) | UserPlayer.objects.filter(player_last_name=query)
		else:
			result = UserPlayer.objects.all()

		return result

class TeamView(generic.DetailView):
	model = Team
	template_name = 'teams/detail.html'

@login_required
def players(request, team_id, player_id):
	player = get_object_or_404(UserPlayer, pk=player_id)
	team = get_object_or_404(Team, pk=team_id)
	form_class = PointForm

	context = {
		'player': player,
		'team': team,
		'points': Point.objects.filter(player=player),
		'form': form_class,
	}
	return render(request, 'players/index.html', context)

@login_required
def add_point(request, player_id):
	form_class = PointForm
	player = get_object_or_404(UserPlayer, pk=player_id)

	if request.method == "POST":
		form = form_class(request.POST, request.FILES)

		if form.is_valid():
			point = form.save(commit=False)
			point.player = player
			point.point_owner = request.user
			point.save()
			player.points_scored += point.point
			player.save()
			build_and_send_email_alert(player, point)
		else:
			return render(request, 'players/index.html', {
				'player': player,
				'team': player.player_team,
				'points': Point.objects.filter(player=player),
				'form': form_class,
				'error_message': "Note is required",
			})

	context = {
		'player': player,
		'team': player.player_team,
		'points': Point.objects.filter(player=player),
		'form': form_class,
	}
	return HttpResponseRedirect(reverse('cloud_roni:players', args=(player.player_team.id, player.id)))

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

@login_required
def update_player(request, player_id):
	player = get_object_or_404(UserPlayer, id=player_id)
	form = UserPlayerForm(request.POST or None, instance=player)

	if form.is_valid():
		form.save()
		context = {
			'player': player,
			'team': player.player_team,
			'points': Point.objects.filter(player=player),
			'form': PointForm,
		}
		return render(request, 'players/index.html', context)

	return render(request, 'players/update.html', {'form': form, 'team': player.player_team})

@login_required
@csrf_exempt
def place_trade(request, team_id):
	requesting_team = get_object_or_404(Team, team_owner=request.user)
	receiving_team = get_object_or_404(Team, id=team_id)

	if request.method == 'POST':
		new_trade = Trade(proposing_team=requesting_team,
						receiving_team=receiving_team,
						created_date=timezone.now(),)
		new_trade.save()
		for player_id in request.POST.getlist('requesting_team_ids[]'):
			player = UserPlayer.objects.get(id=player_id)
			new_trade.proposing_team_players.add(player)
		for player_id in request.POST.getlist('receiving_team_ids[]'):
			player = UserPlayer.objects.get(id=player_id)
			new_trade.receiving_team_players.add(player)
		new_trade.save()
		return JsonResponse({'trade': str(new_trade)})
	
	return render(request, 'teams/trade.html', {'requesting_team': requesting_team, 'receiving_team': receiving_team})

@login_required
def delete_player(request, player_id):
	player = get_object_or_404(UserPlayer, pk=player_id)
	team = player.player_team
	player.delete()

	return HttpResponseRedirect(reverse('cloud_roni:team', args=(team.id,)))

def build_and_send_email_alert(player, point):
	subject = str(player) + ' scored a point!'
	message = (str(point.point_owner) + ' has added a point for ' 
		+ str(player.player_first_name) + ' ' + str(player.player_last_name) + ': ' + str(point.point))

	email_address = player.player_team.team_owner.email

	if email_address == '':
		return

	send_mail(
	    subject,
	    message,
	    'cloud.roni.alerts@gmail.com',
	    [email_address],
	    fail_silently=False,
	)