from django import forms
from django.contrib.auth.models import User
from users.models import PhoneNumber
from django.forms import ModelForm

class UserUpdateForm(ModelForm):
    class Meta:
		model = User
		exclude = ['groups', 'user_permissions', 'is_staff',
		           'is_active', 'is_superuser', 'last_login', 
		           'date_joined', 'password', 'username']

class PhoneNumberForm(ModelForm):
	class Meta:
		model = PhoneNumber
		exclude = ['created_date', 'twilio_formatted_number', 'user', 'is_valid_phone_number']