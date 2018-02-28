from django import forms
from CloudRoni.models import UserPlayer, Team, Point
from django.forms import ModelForm
from leagues.models import League

import pdb

CHOICES=[('HU', 'Heavy Usage'),
         ('MU', 'Moderate Usage'),
         ('LU', 'Light Usage'),
         ('NU', 'Not Using'),]

class UserPlayerForm(ModelForm):
	class Meta:
		model = UserPlayer
		exclude = ['player_team', 'points_scored', 'league']
		
class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = ['created_date', 'team_points', 'league']

    def __init__(self, user, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        league = League.objects.get(participants=user)
        self.fields['team_owner'].queryset = league.participants.all()
        
class PointForm(ModelForm):
    class Meta:
        model = Point
        exclude = ['player', 'point_owner', 'team']