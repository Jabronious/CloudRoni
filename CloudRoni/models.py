from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from django.contrib.auth.models import User

import pdb

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=200)
    created_date = models.DateTimeField('date published')
    team_owner = models.ForeignKey(User)
    team_points = models.IntegerField(default=0)

    def __str__(self):
        return self.team_name

    def players_present(self):
        return UserPlayer.objects.filter(player_team=self).count() > 0

    def filter_team_points(self):
        players = UserPlayer.objects.filter(player_team=self)
        return players.aggregate(Sum('points_scored')).get('points_scored__sum', 0)

    def was_created_recently(self):
        return self.created_date <= timezone.now() - datetime.timedelta(days=1)

class UserPlayer(models.Model):
    HEAVY_USE = 'HU'
    MODERATE_USE = 'MU'
    LIGHT_USE = 'LU'
    NOT_USING = 'NU'
    USAGE_CHOICES = (
        (HEAVY_USE, 'Heavy Use'),
        (MODERATE_USE, 'Moderate Use'),
        (LIGHT_USE, 'Light Use'),
        (NOT_USING, 'Not Using'),
    )
    player_team = models.ForeignKey(Team,
                                    on_delete=models.CASCADE,
                                    null=True)
    player_first_name = models.CharField(max_length=20)
    player_last_name = models.CharField(max_length=20)
    points_scored = models.IntegerField(default=0)
    usage = models.CharField(
        max_length=2,
        choices=USAGE_CHOICES,
        default=NOT_USING,)

    def __str__(self):
        return self.player_first_name + ' ' + self.player_last_name

class Point(models.Model):
    ONE = 1
    MINUS_ONE = -1
    FIVE = 5
    POINT_CHOICES = (
        (ONE, "+1"),
        (MINUS_ONE, "-1"),
        (FIVE, "+5"),
    )
    player = models.ForeignKey(UserPlayer,
                              on_delete=models.CASCADE)
    point = models.IntegerField(
        choices=POINT_CHOICES,
        default=0)
    note = models.TextField(max_length=200)
    point_owner = models.ForeignKey(User)
    team = models.TextField(max_length=200)
    
    def __str__(self):
        return str(self.point)

class Trade(models.Model):
    ACCEPTED = 1
    DECLINED = -1
    PENDING = 0
    OUTCOME_CHOICES = (
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined"),
        (PENDING, "Pending"),
    )
    proposing_team = models.ForeignKey(Team, related_name = "proposing_team")
    receiving_team = models.ForeignKey(Team, related_name = "receiving_team")
    is_completed = models.BooleanField(default=False)
    outcome = models.CharField(
        choices=OUTCOME_CHOICES,
        max_length=10,
        default="Pending")
    created_date = models.DateTimeField()
    proposing_team_players = models.ManyToManyField(UserPlayer, related_name = "proposing_team_players")
    receiving_team_players = models.ManyToManyField(UserPlayer, related_name = "receiving_team_players")
    
    def __str__(self):
        return self.proposing_team.team_name + " -> " + self.receiving_team.team_name

    def update_outcome(self, outcome):
        if(outcome == 'accept'):
            self.outcome = "Accepted"
            #transfer players to proposing team
            proposing_queryset = self.receiving_team_players.all()
            proposing_queryset.update(player_team=self.proposing_team)
            for player in proposing_queryset:
                player.save()
            #transfer players to receiving team
            receiving_queryset = self.proposing_team_players.all()
            receiving_queryset.update(player_team=self.receiving_team)
            for player in receiving_queryset:
                player.save()
        else:
            self.outcome = "Declined"

        self.is_completed = True
        self.save()