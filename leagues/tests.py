# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from leagues.models import League
from django.contrib.auth.models import User
from django.utils import timezone

import pdb

# Create your tests here.
class LeagueViewTests(TestCase):
    def setUp(self):
        self.home_page_request = self.client.get('/')
        user = User.objects.create(username='jab')
        user.set_password('1234')
        user.email = 'test_email@gmail.com'
        user.save()
        self.user = user

    def set_up_league(self):
        new_league = League()
        league = League(name='league', owner=self.user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(self.user)
        league.save()
        self.league = league

    def login_user(self):
        self.client.login(username='jab',password='1234')

    def test_home_page_request_without_sign_in(self):
        content = self.home_page_request.content

        self.assertIn('Welcome to', content)

    def test_home_page_request_with_sign_in_and_in_league(self):
        self.set_up_league()
        self.login_user()
        response = self.client.get('/')

        self.assertRedirects(response, '/cloud_roni/')

    def test_home_page_request_with_sign_in_no_league(self):
        self.login_user()
        response = self.client.get('/')

        self.assertRedirects(response, '/leagues/')

    def test_create_team_get(self):
        response = self.client.get('/create_league/')

        self.assertIn('Create A League', response.content)

    def test_create_team_user_created_league(self):
        self.set_up_league()
        self.login_user()
        response = self.client.post('/create_league/', {'name': 'Wassup',
                                                        'signup_code': 'blahaaaa'})

        self.assertIn('You have already created a league.', response.content)

    def test_create_team_with_invalid_info(self):
        response = self.client.post('/create_league/')

        self.assertIn('Invalid Information', response.content)

    def test_league_index_page_request(self):
        self.set_up_league()
        response = self.client.get('/leagues/')

        self.assertIn('1. league', response.content)

    def test_league_sign_up_correctly(self):
        self.set_up_league()
        self.login_user()
        response = self.client.post('/join_league/', {'code': self.league.signup_code,
                                                     'league_id': str(self.league.id)})

        self.assertJSONEqual(response.content, {'url': '/cloud_roni/'})

    def test_league_sign_up_incorrectly(self):
        self.set_up_league()
        response = self.client.post('/join_league/', {'code': 'ppooooooop',
                                                     'league_id': str(self.league.id)})

        self.assertEqual(response.status_code, 404)
        self.assertIn(response.content, 'Incorrect League Code')

    def test_league_management_page_loads(self):
        self.set_up_league()
        self.login_user()

        response = self.client.get('/manage_league/')

        self.assertInHTML('<input type="text" name="name" value="league" required id="id_name" maxlength="200" />', response.content)
        self.assertInHTML('<input type="text" name="signup_code" value="ehh" required id="id_signup_code" maxlength="15" />', response.content)