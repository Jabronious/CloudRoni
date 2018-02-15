from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = 'league'
urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^create_league/$', views.create_league, name='create_league'),
    url(r'^leagues/$', views.LeaguesListView.as_view(), name='leagues_index'),
    url(r'^join_league/$', views.join_league, name='join_league'),
    url(r'^manage_league/$', views.manage_league, name='manage_league'),
    url(r'^start_new_season/$', views.start_new_season, name='start_new_season'),
    url(r'^terminate_season/$', views.terminate_season, name='terminate_season'),
]