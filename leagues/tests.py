# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from leagues.models import League

# Create your tests here.
class LeagueViewTests(TestCase):
    def setUp(self):
        self.home_page_request = self.client.get('/')

    def team_home_page_request(self):
        content = self.home_page_request.content

        self.assertIn('Welcome to', content)