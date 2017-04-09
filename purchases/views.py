from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from .models import Purchase
from users.models import Member
from games.models import Game

from decimal import Decimal

# Create your views here.
def index(request):
    purchases = Purchase.objects.filter(member=request.user.member).order_by('datetime')

    return render(request, 'purchases/index.html', {'purchases': purchases})


def new(request, gameID):
    if request.method == 'POST':
        if request.user.is_authenticated():
            member = request.user.member
            game = Game.objects.get(pk=gameID)

            rewards_used = Decimal(request.POST['rewards_quantity'])

            purchase = Purchase.objects.create(
                member = member,
                game = game,
                original_amount = game.price,
                discounted_amount = Purchase.get_discounted_amount(game.price, rewards_used),
                billing_method = request.POST['billing_method']
            )

            temp = member.reserved_amount + purchase.discounted_amount
            while (temp >= 100):
                temp -= 100
                member.reward_set.create(member=member)
            member.reserved_amount = temp
            member.use_rewards(rewards_used, purchase)
            member.save()

            member.use_rewards(rewards_used, purchase)

    return redirect(reverse('games:game', kwargs={'id': gameID}))