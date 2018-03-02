from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = 'drafts'
urlpatterns = [
    url(r'^start_draft/$', views.start_draft, name='start_draft'),
    url(r'^draft_player/$', views.draft_player, name='draft_player'),
    url(r'^end_draft/$', views.end_draft, name='end_draft'),
    url(r'^auto_draft/$', views.auto_draft, name='auto_draft'),
    url(r'^draft_results/$', views.draft_results, name='draft_results'),
]