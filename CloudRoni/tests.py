import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from .models import Team, UserPlayer, Point
from . import views
from django.contrib.auth.models import User
import pdb

class TeamModelTests(TestCase):

    def test_was_created_recently(self):
        user = User(username='jr.merryman', password='rabble')
        user.save()
        time = timezone.now() + datetime.timedelta(days = 30)
        team = Team(created_date=time, id=1, team_owner=user)
        team.save()

        self.assertIs(team.was_created_recently(), False)

    def test_team_has_players(self):
        user = User(username='jr.merryman', password='rabble')
        user.save()
        team = Team(created_date=timezone.now(), id=1, team_owner=user)
        team.save()
        player = UserPlayer(player_team=team, id=1)
        player.save()

        self.assertIs(team.players_present(), True)

    def test_team_has_no_players(self):
        user = User(username='jr.merryman', password='rabble')
        user.save()
        team = Team(created_date=timezone.now(), id=1, team_owner=user)
        team.save()

        self.assertIs(team.players_present(), False)

    def test_filter_points(self):
        user = User(username='jr.merryman', password='rabble')
        user.save()
        team = Team(created_date=timezone.now(), id=1, team_owner=user)
        team.save()
        player = UserPlayer(player_team=team, id=1, points_scored=1)
        player.save()

        self.assertIs(team.filter_team_points(), 1)

class CloudRoniViewsTests(TestCase):
    
    def test_root_url_resolves_to_teams(self):
        found = resolve('/')
        self.assertEqual(found.url_name, 'index')

    #def test_teams_page_has_correct_info(self):
    #    request = HttpRequest()
    #    pdb.set_trace()
    #    response = views.IndexView(request)
        