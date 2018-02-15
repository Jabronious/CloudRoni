from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from leagues.models import League
from django.utils import timezone

import pdb

@periodic_task(crontab(minute='*/1'))
def end_league_season():
    pdb.set_trace()
    leagues = League.objects.filter(end_date__date=timezone.now().date())
    
