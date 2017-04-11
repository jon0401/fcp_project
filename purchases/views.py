from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Purchase
from users.models import Member
from games.models import Game

from decimal import Decimal

# Create your views here.
@login_required
def index(request):
    purchases = Purchase.objects.filter(member=request.user.member).order_by('datetime')

    return render(request, 'purchases/index.html', {'purchases': purchases})

@login_required
def new(request, gameID):
    if request.method == 'POST':
        if request.user.is_authenticated():
            member = request.user.member
            game = Game.objects.get(pk=gameID)

            if not member.has_purchased(game):
                rewards_used = Decimal(request.POST['rewards_quantity'])

                purchase = Purchase.objects.create(
                    member = member,
                    game = game,
                    original_amount = game.price,
                    discounted_amount = Purchase.get_discounted_amount(game.price, rewards_used),
                    billing_method = request.POST['billing_method']
                )
                member.use_rewards(rewards_used, purchase)
                purchase.issue_rewards(member)
                
    return redirect(reverse('games:game', kwargs={'id': gameID}))