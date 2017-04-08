"""fcp_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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

    url(r'^$', games_views.index, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
