from django.shortcuts import render,redirect
from django.conf import settings
from .models import Game
from rewards.models import Reward
from users.models import Member
from tags.forms import TagForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    else:
        if not Member.objects.filter(user=request.user):
            member = Member(user=request.user, display_name=request.user.username)
            member.save()
        featured_games = Game.objects.filter(featured=True)
        rewards = Reward.objects.filter(member=request.user.member, purchase__isnull=True)
        recommended_games = request.user.member.get_recommended_games()

        return render(request, 'games/index.html', {'featured_games': featured_games, 'rewards': rewards, 'recommended_games': recommended_games})

def show(request, id):
    game = Game.objects.get(pk=id)
    tag_form = TagForm()

    for orgg in request.user.member.reward_set.all():
        orgg.checking()
    request.user.member.reward_set.all().filter(check=True).delete()
    request.user.member.save()

    rewards = Reward.objects.filter(member=request.user.member, purchase__isnull=True)
    return render(request, 'games/show.html', {'game': game, 'tag_form': tag_form, 'rewards': rewards})