from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='purchases'),
    url(r'^new/(?P<gameID>\d+)$', views.new, name='new'),
]