from django.shortcuts import render

from .models import Genre
from games.models import Game

# Create your views here.
def index(request):
    genres = Genre.objects.all().order_by('name')

    return render(request, 'genres/index.html', {'genres': genres})

def show(request, name):
    genre = Genre.objects.get(name=name)
    games = Game.objects.filter(genre=genre).order_by('release_datetime')

    return render(request, 'genres/show.html', {'genre': genre, 'games': games})
