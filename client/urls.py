
from django.conf.urls import url

from client import views

urlpatterns = [
    url('^download', views.download_client, name='download-cmt-client'),
]