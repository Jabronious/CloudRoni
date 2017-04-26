from django.contrib import admin

from .models import Team, UserPlayer

# Register your models here.

admin.site.register(Team)
admin.site.register(UserPlayer)
