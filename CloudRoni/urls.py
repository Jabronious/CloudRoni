from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = 'cloud_roni'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: CloudRoni/5/team
    url(r'^(?P<pk>[0-9]+)/team/$', views.TeamView.as_view(), name='team'),
     # ex: CloudRoni/34/players/2/
    url(r'^(?P<team_id>[0-9]+)/players/(?P<player_id>[0-9]+)/$', views.players, name='players'),
    # ex: CloudRoni/2/create_player
    url(r'^(?P<team_id>[0-9]+)/create_player/$', views.create_player, name='create_player'),
    # ex: CloudRoni/create_team
    url(r'^create_team/$', views.create_team, name='create_team'),
    # ed: CloudRoni/update_player
    url(r'^(?P<player_id>[0-9]+)/update_player/$', views.update_player, name='update_player'),
    # ex: CloudRoni/55/delete_player
    url(r'^(?P<player_id>[0-9]+)/delete_player/$', views.delete_player, name='delete_player'),
    # ex: CloudRoni/55/add_point
    url(r'^(?P<player_id>[0-9]+)/add_point/$', views.add_point, name='add_point'),
    url(r'^players/$', views.PlayersView.as_view(), name='all_players'),
    url(r'^(?P<team_id>[0-9]+)/trade/$', views.place_trade, name='place_trade'),
    url(r'^trades/$', views.TradesView.as_view(), name='my_trades'),
    url(r'^complete_trade/$', views.complete_trade, name='complete_trade'),
    url(r'^rules/$', views.rules, name='rules'),
]
