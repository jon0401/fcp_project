from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Game
from rewards.models import Reward
from users.models import Member
from tags.forms import TagForm

@login_required
def index(request):
    if not Member.objects.filter(user=request.user):
        member = Member(user=request.user, display_name=request.user.username)
        member.save()

    member = request.user.member
    member.remove_expired_rewards

    featured_games = Game.objects.filter(featured=True)
    rewards = Reward.objects.filter(member=member, purchase__isnull=True)
    recommended_games = member.get_recommended_games()

    return render(request, 'games/index.html', {'featured_games': featured_games, 'rewards': rewards, 'recommended_games': recommended_games, 'member': member})

@login_required
def show(request, id):
    member = request.user.member
    member.remove_expired_rewards()

    game = Game.objects.get(pk=id)
    tag_form = TagForm()
    rewards = Reward.objects.filter(member=member, purchase__isnull=True)
    
    return render(request, 'games/show.html', {'game': game, 'tag_form': tag_form, 'rewards': rewards})