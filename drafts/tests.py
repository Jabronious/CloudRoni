# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.urls import reverse
from django.core import mail

from CloudRoni.models import Team, UserPlayer
from . import views
from django.contrib.auth.models import User
from leagues.models import League
from drafts.models import Draft, Drafter
import pdb

# Create your tests here.
class DraftViewsTests(TestCase):
    def setUp(self):
        user = User(username='jr.merryman')
        user.set_password('rabble')
        user.save()
        self.user = user
        league = League(name='league', owner=user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(user)
        league.save()
        self.league = league

        #second user
        second_user = User.objects.create(username='jabroni')
        second_user.set_password('1234')
        second_user.save()

        #third user
        third_user = User.objects.create(username='asdf')
        third_user.set_password('1234')
        third_user.save()

        #set up league for new users
        league.participants.add(second_user)
        league.participants.add(third_user)
        league.save()
        
        #first team with players
        first_team = Team(team_name='jabs', team_owner_id=user.id, created_date=timezone.now(), league=self.league)
        first_team.save()
        self.first_team = first_team

        #second team with players
        second_team = Team(team_name='jabronis', team_owner_id=second_user.id, created_date=timezone.now(), league=self.league)
        second_team.save()
        self.second_team = second_team

        #second team with players
        third_team = Team(team_name='asdf', team_owner_id=third_user.id, created_date=timezone.now(), league=self.league)
        third_team.save()

    def login_user(self):
        self.client.login(username='jr.merryman', password='rabble')

    def test_start_draft(self):
        self.login_user()
        #upload players
        myfile = open('csv_upload/csv_test_file.csv','r') 
        self.client.post('/csv/upload/csv/', {'csv_file':myfile})
        
        response = self.client.get('/draft/start_draft/')

        self.assertTrue('Current Drafting Team' in response.content)
        self.assertEqual(Draft.objects.all().count(), 1)
        self.assertEqual(Drafter.objects.filter(league=self.league).count(), Team.objects.filter(league=self.league).count())

    def test_start_draft_with_draft_already(self):
        self.login_user()
        #upload players
        myfile = open('csv_upload/csv_test_file.csv','r') 
        self.client.post('/csv/upload/csv/', {'csv_file':myfile})
        
        self.client.get('/draft/start_draft/')

        response = self.client.get('/draft/start_draft/')

        self.assertTrue('Current Drafting Team' in response.content)
        self.assertEqual(Draft.objects.all().count(), 1)
        self.assertEqual(Drafter.objects.filter(league=self.league).count(), Team.objects.filter(league=self.league).count())

    def test_start_draft_without_team_or_players(self):
        self.login_user()

        response = self.client.get('/draft/start_draft/')

        self.assertTrue('You need more players/teams to start a draft' in response.content)
        self.assertEqual(Draft.objects.all().count(), 0)

    def test_draft_player(self):
        self.login_user()
        #upload players
        myfile = open('csv_upload/csv_test_file.csv','r') 
        self.client.post('/csv/upload/csv/', {'csv_file':myfile})
        
        self.client.get('/draft/start_draft/')
        draft = Draft.objects.last()
        player = UserPlayer.objects.first()
        current_team = draft.current_team
        current_drafter_position = Drafter.objects.get(team=current_team).position
        
        response = self.client.post('/draft/draft_player/', {'player_id': str(player.id),
                                                             'team_id': str(current_team.id) 
                                                            })
        draft = Draft.objects.last()
        player = UserPlayer.objects.get(id=player.id)

        self.assertTrue(player.player_team == current_team)
        self.assertEqual(draft.current_team, Drafter.objects.get(league=self.league, position=current_drafter_position+1).team)
        self.assertIn('"current_team_name": "' + str(draft.current_team) + '"', response.content)

    def test_draft_player_with_no_more_players(self):
        self.login_user()
        #upload players
        myfile = open('csv_upload/csv_test_file.csv','r') 
        self.client.post('/csv/upload/csv/', {'csv_file':myfile})
        
        self.client.get('/draft/start_draft/')
        all_players = UserPlayer.objects.all()
        for player in all_players:
            player.player_team = self.first_team
            player.save()
        player = UserPlayer.objects.last()
        player.player_team = None
        player.save()
        draft = Draft.objects.last()
        
        response = self.client.post('/draft/draft_player/', {'player_id': str(player.id),
                                                             'team_id': str(draft.current_team.id) 
                                                            })

        self.assertJSONEqual(response.content, {'ended': True,'url': reverse('drafts:end_draft')})