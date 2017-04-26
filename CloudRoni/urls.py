from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: CloudRoni/5/
    url(r'^(?P<team_id>[0-9]+)/$', views.team, name='team'),
     # ex: CloudRoni/34/players/2/
    url(r'^(?P<team_id>[0-9]+)/players/(?P<player_id>[0-9]+)/$', views.players, name='players'),
]
