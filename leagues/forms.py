from django import forms
from leagues.models import League
from django.forms import ModelForm

class LeagueForm(ModelForm):
	class Meta:
		model = League
		exclude = ['created_date', 'participants', 'owner',]