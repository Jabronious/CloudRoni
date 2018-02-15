from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from leagues.models import League
from django.utils import timezone
from leagues.views import end_season
from CloudRoni.models import Team

import pdb

@periodic_task(crontab(minute=0, hour=0))
def end_league_season():
    leagues = League.objects.filter(end_date__date=timezone.now().date())
    for league in leagues:
        if Team.objects.filter(league=league).count() < 3:
            continue
        end_season(league)