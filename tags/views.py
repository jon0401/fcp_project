from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from .models import Tag
from .forms import TagForm
from games.models import Game

# Create your views here.
def index(request):
    tags = Tag.objects.all().order_by('name')

    return render(request, 'tags/index.html', {'tags': tags})

def show(request, name):
    tag = Tag.objects.get(name=name)
    games = Game.objects.filter(tags__in=[tag]).order_by('release_datetime')

    return render(request, 'tags/show.html', {'tag': tag, 'games': games})

def new(request, gameID):
    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():
            game = Game.objects.get(pk=gameID)
            tags = Tag.objects.filter(name=form.cleaned_data.get('name'))

            if tags.count() > 0:
                tag = tags[0]
            else:
                tag = form.save(commit=False)

            tag.save()
            game.tags.add(tag)
  
    return redirect(reverse('games:game', kwargs={'id': gameID}))