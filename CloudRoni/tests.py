import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from .models import Team, UserPlayer, Point
from . import views
from .forms import UserPlayerForm, TeamForm, PointForm
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
    
    def setUp(self):
        self.home_page_request = self.client.get('/')
        user = User.objects.create(username='jab')
        user.set_password('1234')
        user.save()
        self.new_user = user
    
    def login_user(self):
        self.client.login(username='jab',password='1234')
        
    def set_up_team_with_players(self):
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now())
        team.save()
        self.team = team
        player = UserPlayer(player_team=team, player_first_name='joe', player_last_name='momma')
        player.save()
        self.player = player
    
    def test_root_url_resolves_to_teams(self):
        found = resolve('/')
        self.assertEqual(found.url_name, 'index')

    def test_teams_page_has_correct_info_with_no_teams(self):
        content = self.home_page_request.content
        self.assertIn('These are not the teams you are looking for...', content)
        
    def test_teams_page_has_correct_info_with_teams(self):
        Team(team_name='jabs', team_owner_id=1, created_date=timezone.now()).save()
        reload_home_page = self.client.get('/')
        self.assertIn('<a href="/1/team/">jabs</a>', reload_home_page.content)
    
    def test_teams_page(self):
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now())
        team.save()
        UserPlayer(player_team=team, player_first_name='joe', player_last_name='momma').save()
        team_page_request = self.client.get("/" + str(team.id) + "/team/")
        self.assertIn('joe momma', team_page_request.content)
        
    def test_detailed_player_view(self):
        self.set_up_team_with_players()
        self.login_user()
        player_page_request = self.client.get("/" + str(self.player.player_team.id) + "/players/" + str(self.player.id) + "/")
        self.assertIn('joe momma', player_page_request.content)

    def test_add_point(self):
        self.set_up_team_with_players()
        self.login_user()
        form = PointForm({
            'point': Point.ONE,
            'note': 'Hey, I am a note',
        })
        
        self.assertTrue(form.is_valid())
        
        submitted_point = form.save(commit=False)
        submitted_point.player = self.player
        submitted_point.point_owner = self.new_user
        submitted_point.save()
        
        self.assertEqual(submitted_point.player, self.player)
        self.assertEqual(submitted_point.point, Point.ONE)
        self.assertEqual(submitted_point.note, "Hey, I am a note")
        self.assertEqual(submitted_point.point_owner, self.new_user)