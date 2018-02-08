# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
class LeagueViewTests(TestCase):
    def test_teams_page_has_correct_info_with_no_teams(self):
        content = self.home_page_request.content

        self.assertIn('Welcome to', content)