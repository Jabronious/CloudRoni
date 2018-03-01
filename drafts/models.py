# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from django.contrib.auth.models import User
from CloudRoni.models import Team, UserPlayer
from leagues.models import League

# Create your models here.
class Draft(models.Model):
    league = models.ForeignKey(League)
    started_date = models.DateTimeField('started')
    current_team = models.ForeignKey(Team, null=True, blank=True)
    next_team = models.IntegerField(null=True, blank=True)
    end_turn_timer = models.DateTimeField('timer')

class Drafter(models.Model):
    team = models.OneToOneField(Team)
    position = models.IntegerField()
    league = models.ForeignKey(League)
    draft = models.ForeignKey(Draft)