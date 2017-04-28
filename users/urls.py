from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # url(r'^$', views.index, name='users'),
    # url(r'^(?P<name>\w+)$', views.show, name='user'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^register/$',views.UserFormView.as_view(), name ='register'),

    url(r'^update/$', views.UserUpdate.as_view(), name = 'update'),

    url(r'logout/$',views.logout_view, name ='logout_view'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),


]