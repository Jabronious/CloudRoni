# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response

from django.shortcuts import render

from leagues.forms import LeagueForm
from CloudRoni.models import Team, UserPlayer, Point
from CloudRoni.forms import UserPlayerForm
from django.contrib.auth.decorators import login_required

import pdb
import re

# Create your views here.

@login_required
def upload_csv(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if "GET" == request.method:
        return render(request, "csv_upload.html", {'team': team})
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            error_message = 'File is not CSV type'
            return render(request, 'team/detail.html', {
				'team': team,
				'error_message': error_message,
			})

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\r")
        if len(lines) == 1:
            lines = file_data.split("\n")

        headers = {}
        for line in lines:
            fields = line.split(",")
            if lines[0] == line:
                headers['first'] = fields[0].strip()
                headers['second'] = fields[1].strip()
                fields[2] = fields[2].replace('\r', '')
                headers['third'] = fields[2].strip()
            else:
                player_hash = {}
                player_hash[headers['first']] = fields[0].strip()
                player_hash[headers['second']] = fields[1].strip()
                fields[2] = fields[2].replace('\r', '')
                player_hash[headers['third']] = fields[2].strip()
                try:
                    obj, created = UserPlayer.objects.get_or_create(
                        player_first_name=player_hash['player_first_name'],
                        player_last_name=player_hash['player_last_name'],
                        usage=player_hash['usage'],
                        player_team=team,
                        )
                except Exception as e:
                    pass

        return HttpResponseRedirect(reverse('cloud_roni:team', args=(team.id,)))

    except Exception as e:
        return HttpResponseRedirect(reverse('cloud_roni:team', args=(team.id,)))

@login_required
def admin_upload_csv(request):
    if "GET" == request.method:
        return render(request, "admin_csv_upload.html")
    # if not GET, then proceed
    try:
        form = LeagueForm(request.POST or None, instance=request.user.league)
        league = request.user.league
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            error_message = 'File is not CSV type'
            return render(request, 'leagues/league_management.html', {
                'form': form,
				'confirmation': error_message,
			})

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\r")
        if len(lines) == 1:
            lines = file_data.split("\n")

        headers = {}
        for line in lines:
            fields = line.split(",")
            if lines[0] == line:
                headers['first'] = fields[0].strip()
                headers['second'] = fields[1].strip()
                fields[2] = fields[2].replace('\r', '')
                headers['third'] = fields[2].strip()
            else:
                player_hash = {}
                player_hash[headers['first']] = fields[0].strip()
                player_hash[headers['second']] = fields[1].strip()
                fields[2] = fields[2].replace('\r', '')
                player_hash[headers['third']] = fields[2].strip()
                try:
                    obj, created = UserPlayer.objects.get_or_create(
                        player_first_name=player_hash['player_first_name'],
                        player_last_name=player_hash['player_last_name'],
                        usage=player_hash['usage'],
                        league=league,
                        )
                except Exception as e:
                    pass

        return render(request, 'leagues/league_management.html', {'form': form, 'confirmation': ''})

    except Exception as e:
        return HttpResponseRedirect(reverse('cloud_roni:index'))