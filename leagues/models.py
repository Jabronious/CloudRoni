# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class League(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(User)
    participants = models.ManyToManyField(User, related_name='participants')
    created_date = models.DateTimeField('date created')
    signup_code = models.CharField(max_length=15, unique=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Winner(models.Model):
    individual = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)

class Season(models.Model):
    first = models.ForeignKey(Winner, related_name='first')
    second = models.ForeignKey(Winner, related_name='second')
    thrid = models.ForeignKey(Winner, related_name='third')
    league = models.ForeignKey(League)