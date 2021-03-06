# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from CloudRoni.models import Team, UserPlayer, Point
from leagues.models import League
from django.utils import timezone
from django.urls import reverse

import pdb

# Create your tests here.
class CsvUploadsTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='jab')
        user.set_password('1234')
        user.email = 'test_email@gmail.com'
        user.save()
        self.new_user = user
        league = League(name='league', owner=user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(user)
        league.save()
        self.league = league

    def login_user(self):
        self.client.login(username='jab',password='1234')
        
    def set_up_team(self):
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now(), league=self.league)
        team.save()
        self.team = team
        
    def test_csv_upload(self):
        self.login_user()
        self.set_up_team()
        myfile = open('csv_upload/csv_test_file.csv','r') 
        response = self.client.post('/csv/' + str(self.team.id) + '/upload/csv/', {'csv_file':myfile})

        self.assertIs(self.team.players_present(), True)
        self.assertRedirects(response, expected_url=reverse('cloud_roni:team', args=(self.team.id,)))

    def test_csv_upload_without_csv(self):
        self.login_user()
        self.set_up_team()
        myfile = open('csv_upload/views.py','r') 
        response = self.client.post('/csv/' + str(self.team.id) + '/upload/csv/', {'csv_file':myfile})

        self.assertIn('File is not CSV type', response.content)
    
    def test_get_csv_upload(self):
        self.login_user()
        self.set_up_team()
        response = self.client.get('/csv/' + str(self.team.id) + '/upload/csv/')

        self.assertIn('<input class=\'inputfile\' type="file" name="csv_file" id="csv_file" required="True">', response.content)

    def test_admin_csv_upload(self):
        self.login_user()
        myfile = open('csv_upload/csv_test_file.csv','r') 
        response = self.client.post('/csv/upload/csv/', {'csv_file':myfile})

        self.assertIs(self.league.league_player_count() > 0, True)
        self.assertIn('League Management', response.content)

    def test_admin_csv_upload_without_csv(self):
        self.login_user()
        myfile = open('csv_upload/views.py','r') 
        response = self.client.post('/csv/upload/csv/', {'csv_file':myfile})

        self.assertIn('File is not CSV type', response.content)
    
    def test_get_admin_csv_upload(self):
        self.login_user()
        response = self.client.get('/csv/upload/csv/')

        self.assertIn('<input class=\'inputfile\' type="file" name="csv_file" id="csv_file" required="True">', response.content)