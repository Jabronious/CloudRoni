from django import forms
from CloudRoni.models import UserPlayer
from django.forms import ModelForm

CHOICES=[('HU', 'Heavy Usage'),
         ('MU', 'Moderate Usage'),
         ('LU', 'Light Usage'),
         ('NU', 'Not Using'),]

class UserPlayerForm(ModelForm):
	class Meta:
		model = UserPlayer
		exclude = ['player_team', 'points_scored']
