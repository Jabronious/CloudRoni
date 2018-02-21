from django import forms
from leagues.models import League
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
import pdb

class LeagueForm(ModelForm):
	end_date = forms.DateField(widget=forms.SelectDateWidget())
	
	def clean_end_date(self):
		data = self.cleaned_data['end_date']

		#Check date is not in past. 
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - date is in the past'))

		#Check date is in range librarian allowed to change (+4 weeks).
		if data < datetime.date.today() + datetime.timedelta(weeks=1):
			raise ValidationError(_('Invalid date - league time is too short (1 week or more)'))

		# Remember to always return the cleaned data.
		return data

	class Meta:
		model = League
		exclude = ['created_date', 'participants', 'owner', 'ended']