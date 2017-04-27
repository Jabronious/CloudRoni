from django.conf.urls import url

from . import views

app_name = 'cloud_roni'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<team_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: CloudRoni/5/team
    url(r'^(?P<team_id>[0-9]+)/team/$', views.team, name='team'),
     # ex: CloudRoni/34/players/2/
    url(r'^(?P<team_id>[0-9]+)/players/(?P<player_id>[0-9]+)/$', views.players, name='players'),
]
