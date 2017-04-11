from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Game
from rewards.models import Reward
from users.models import Member
from tags.forms import TagForm

@login_required
def index(request):
    if Member.objects.filter(user=request.user) is None:
        member = Member(user=request.user, display_name=request.user.username)
        member.save()
    featured_games = Game.objects.filter(featured=True)
    rewards = Reward.objects.filter(member=request.user.member, purchase__isnull=True)
    recommended_games = request.user.member.get_recommended_games()

    return render(request, 'games/index.html', {'featured_games': featured_games, 'rewards': rewards, 'recommended_games': recommended_games})

@login_required
def show(request, id):
    game = Game.objects.get(pk=id)
    tag_form = TagForm()

    request.user.member.remove_expired_rewards()

    rewards = Reward.objects.filter(member=request.user.member, purchase__isnull=True)
    return render(request, 'games/show.html', {'game': game, 'tag_form': tag_form, 'rewards': rewards})