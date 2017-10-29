from django.conf.urls import url

from . import views

app_name = 'csv_upload'
urlpatterns = [
    url(r'^(?P<team_id>[0-9]+)/upload/csv/$', views.upload_csv, name='upload_csv'),   
]