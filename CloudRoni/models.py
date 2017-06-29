from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=200)
    created_date = models.DateTimeField('date published')

    def __str__(self):
        return self.team_name

    def was_created_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1)

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
                                    on_delete=models.CASCADE)
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