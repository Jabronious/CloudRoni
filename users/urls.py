from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<user_id>[0-9]+)/account/$', views.update_account, name='account'),
    url(r'^update_phone_number/$', views.create_or_update_phone_number, name='create_or_update_phone_number'),
]
