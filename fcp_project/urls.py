from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from games import views as games_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^games/', include('games.urls', namespace="games")),
    url(r'^tags/', include('tags.urls', namespace="tags")),
    url(r'^purchases/', include('purchases.urls', namespace="purchases")),
    url(r'^rewards/', include('rewards.urls', namespace="rewards")),
    url(r'^genres/', include('genres.urls', namespace="genres")),
    url(r'^users/', include('users.urls', app_name="users", namespace="users")),

    url(r'^$', games_views.index, name='home'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
