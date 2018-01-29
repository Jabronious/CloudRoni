# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-29 18:43
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Sum

def update_team_points(apps, schema_editor):
    Team = apps.get_model('CloudRoni', 'Team')
    UserPlayer = apps.get_model('CloudRoni', 'UserPlayer')
    for team in Team.objects.all():
        players = UserPlayer.objects.filter(player_team=team)
        team.team_points = players.aggregate(Sum('points_scored')).get('points_scored__sum', 0)
        team.save()

class Migration(migrations.Migration):

    dependencies = [
        ('CloudRoni', '0013_point_team'),
    ]

    operations = [
        migrations.RunPython(update_team_points),
    ]