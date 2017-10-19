# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response

from django.shortcuts import render

from CloudRoni.models import Team, UserPlayer, Point
from CloudRoni.forms import UserPlayerForm

import pdb
import re

# Create your views here.
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