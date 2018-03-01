# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
import pdb
# Create your models here.

class League(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(User)
    participants = models.ManyToManyField(User, related_name='participants')
    created_date = models.DateTimeField('date created')
    signup_code = models.CharField(max_length=15, unique=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField(default=False)
    drafted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_players_available(self):
        Team = apps.get_model('CloudRoni', 'Team')
        team_player_count = 0
        for team in Team.objects.filter(league=self):
            team_player_count += team.get_player_set().count()

        return team_player_count == self.league_player_count()

    def league_player_count(self):
        UserPlayer = apps.get_model('CloudRoni', 'UserPlayer')
        return UserPlayer.objects.filter(league=self).count()

class Winner(models.Model):
    individual = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)

class Season(models.Model):
    first = models.ForeignKey(Winner, related_name='first')
    second = models.ForeignKey(Winner, related_name='second')
    third = models.ForeignKey(Winner, related_name='third')
    league = models.ForeignKey(League)