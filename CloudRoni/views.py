from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Team, UserPlayer
 
def index(request):
	teams_list = Team.objects.order_by('-created_date')[:10]
	template = loader.get_template('teams/index.html')
	context = {
		'teams_list': teams_list,
	}
	return HttpResponse(template.render(context, request))

def team(request, team_id):
	response = "Here is a team %s!"
	return HttpResponse(response % team_id)

def players(request, team_id, player_id):
	return HttpResponse("Here is a player {} from team # {}".format(player_id, team_id))