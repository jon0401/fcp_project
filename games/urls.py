from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='games'),
    url(r'^(?P<id>\d+)$', views.show, name='game'),
]