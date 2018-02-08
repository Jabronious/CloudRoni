from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import loader, RequestContext
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.models import PhoneNumber
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from leagues.models import League

from twilio.rest import Client


from CloudRoni.models import Team, UserPlayer, Point, Trade
from CloudRoni.forms import UserPlayerForm, TeamForm, PointForm

import pdb

class IndexView(generic.ListView):
	template_name = 'teams/index.html'
	context_object_name = 'teams_list'

	def get_queryset(self):
		"""Return all teams ordered by team_points"""
		league = League.objects.filter(participants=self.request.user)
		return Team.objects.filter(league=league).order_by('-team_points').reverse()

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

class TradesView(generic.ListView):
	template_name = 'teams/trades_index.html'
	context_object_name = 'trade_list'

	def get_queryset(self):
		team = Team.objects.get(team_owner=self.request.user)
		result = Trade.objects.filter(receiving_team=team) | Trade.objects.filter(proposing_team=team)
		return result

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
			point.team = str(player.player_team)
			point.save()
			player.points_scored += point.point
			player.save()
			player.player_team.team_points += point.point
			player.player_team.save()

			build_and_send_email_alert(player, point)

			try:
				number = PhoneNumber.objects.get(user=player.player_team.team_owner)
				if number.is_valid_phone_number:
					message = str(player) + ": received " + str(point) + " point(s)"
					send_sms(number, message)
			except:
				pass
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
	if request.method == 'POST':
		form = TeamForm(request.user, request.POST)
		if form.is_valid():
			new_team = form.save(commit=False)
			new_team.created_date = timezone.now()
			new_team.league = League.objects.get(participants=request.user)
			new_team = form.save()

			return HttpResponseRedirect(reverse('cloud_roni:index'))
		else:
			form_class = TeamForm(request.user)
			return render(request, 'teams/create.html', {
					'form': form_class,
					'error_message': "Invalid Information!",
				})

	form_class = TeamForm(request.user)
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

		try:
			number = PhoneNumber.objects.get(user=receiving_team.team_owner)
			if number.is_valid_phone_number:
				message = "A trade has been received by " + str(requesting_team)
				send_sms(number, message)
		except:
			pass
		new_trade.save()


		return JsonResponse({'trade': str(new_trade)})
	
	return render(request, 'teams/trade.html', {'requesting_team': requesting_team, 'receiving_team': receiving_team})

@login_required
@csrf_exempt
def complete_trade(request):
	trade = get_object_or_404(Trade, id=request.POST.get('trade_id'))
	outcome = request.POST.get('outcome')

	trade.update_outcome(outcome)

	try:
		number = PhoneNumber.objects.get(user=trade.proposing_team.team_owner)
		if number.is_valid_phone_number:
			message = str(trade.receiving_team) + " has " + trade.outcome.lower() + " your trade."
			send_sms(number, message)
	except:
		pass

	return JsonResponse({'outcome': trade.outcome})

@login_required
def delete_player(request, player_id):
	player = get_object_or_404(UserPlayer, pk=player_id)
	team = player.player_team
	player.delete()

	return HttpResponseRedirect(reverse('cloud_roni:team', args=(team.id,)))

def build_and_send_email_alert(player, point):
	email_address = player.player_team.team_owner.email

	if email_address == '':
		return

	subject = str(player) + ' scored a point!'
	message = (str(point.point_owner) + ' has added a point for '
		+ str(player.player_first_name) + ' ' + str(player.player_last_name) + ': ' + str(point.point))

	send_mail(
	    subject,
	    message,
	    'cloud.roni.alerts@gmail.com',
	    [email_address],
	    fail_silently=False,
	)

def send_sms(to, message):
    client = Client(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(
        body=message, to=to.twilio_formatted_number, from_=settings.TWILIO_NUMBER)
    return response