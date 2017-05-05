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
		#fields = '__all__'
		exclude = ['player_team', 'points_scored']
	"""player_first_name = forms.CharField(required=True)
	player_last_name = forms.CharField(required=True)
	usage = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())"""
