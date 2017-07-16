import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Team, UserPlayer, Point

class TeamModelTests(TestCase):
    
    def test_was_created_recently(self):
        time = timezone.now() + datetime.timedelta(days = 30)
        future_team = Team(created_date = time)
        
        self.assertIs(future_team.was_created_recently(), False)