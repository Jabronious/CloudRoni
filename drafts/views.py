# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader, RequestContext
from django.urls import reverse
from django.shortcuts import render
from CloudRoni.models import Team, UserPlayer
from drafts.models import Draft, Drafter
from django.utils import timezone
from leagues.forms import LeagueForm
from django.views.decorators.csrf import csrf_exempt
import datetime
import random

import pdb
# Create your views here.
def start_draft(request):
    league = request.user.league

    teams = Team.objects.filter(league=league)
    players = UserPlayer.objects.filter(league=league)

    if teams.count() < 3 or not players.count() > 0:
        form = LeagueForm(request.POST or None, instance=request.user.league)
        confirmation = 'You need more players/teams to start a draft'
        return render(request, 'leagues/league_management.html', {'form': form, 'confirmation': confirmation})

    try:
        draft = Draft.objects.get(league=league)
        
        context = {
            'teams_list': teams,
            'draft': draft,
            'initial': Drafter.objects.get(league=league, team=draft.current_team),
            'players_list': UserPlayer.objects.filter(league=league),
        }

    except ObjectDoesNotExist:
        draft = Draft(league=league,
                        started_date=timezone.now(),
                        end_turn_timer=timezone.now() + datetime.timedelta(minutes=3)
                        )
        draft.save()
        position_arr = random.sample(xrange(1,teams.count()+1), teams.count())
        for team in teams:
            drafter = Drafter(team=team,
                                position=position_arr.pop(),
                                league=league,
                                draft=draft)
            drafter.save()

        draft.current_team = Drafter.objects.get(league=league, position=1).team
        draft.next_team = 2
        draft.save()
        
        league.drafted = True
        league.save()

        context = {
            'teams_list': teams,
            'draft': draft,
            'initial': Drafter.objects.get(league=league, position=1),
            'players_list': UserPlayer.objects.filter(league=league),
        }
    
    return render(request, 'drafts/draft_dashboard.html', context)

@csrf_exempt
def draft_player(request):
    team = Team.objects.get(id=int(request.POST.get('team_id')))

    player = UserPlayer.objects.get(id=int(request.POST.get('player_id')))
    player.player_team = team
    player.save()
    
    league = request.user.league
    teams = Team.objects.filter(league=league)
    if league.is_players_available():
        return JsonResponse({
            'ended': True,
            'url': reverse('drafts:end_draft'),
        })
    
    draft = Draft.objects.get(league=league)
    try:
        position = draft.next_team
        current_team = Drafter.objects.get(league=league, position=position)
        draft.next_team += 1
    except ObjectDoesNotExist:
        draft.next_team = 2
        current_team = Drafter.objects.get(league=league, position=1)

    draft.current_team = current_team.team
    draft.end_turn_timer = timezone.now() + datetime.timedelta(minutes=3)
    draft.save()
    
    try:
        player_list = []
        for solo_player in UserPlayer.objects.filter(player_team=current_team.team):
            player_list.append(str(solo_player))
    except:
        player_list = {}

    teams_player_list = {}
    for individual_team in teams:
        teams_player_list[str(individual_team)] = []
        for team_player in individual_team.get_player_set():
            teams_player_list[str(individual_team)].append(str(team_player))

    return JsonResponse({
        'current_team_name': str(current_team.team),
        'current_team_id': current_team.team.id,
        'end_time': draft.end_turn_timer,
        'current_team_players': player_list,
        'drafted_player_id': player.id,
        'teams_player_list': teams_player_list,
    })

@csrf_exempt
def end_draft(request):
    Draft.objects.get(league=request.user.league).delete()
    return JsonResponse({'url': reverse('cloud_roni:index')})