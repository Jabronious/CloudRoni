from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class UserUpdateForm(ModelForm):
    class Meta:
		model = User
		exclude = ['groups', 'user_permissions', 'is_staff',
		           'is_active', 'is_superuser', 'last_login', 
		           'date_joined', 'password']