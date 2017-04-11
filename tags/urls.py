from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='tags'),
    url(r'^(?P<name>[\w\-]+)$', views.show, name='tag'),
    url(r'^new/(?P<gameID>\d+)$', views.new, name='new'),
]