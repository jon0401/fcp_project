from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Purchase
from payments.models import Payment
from users.models import Member
from games.models import Game

from decimal import Decimal
from django.core.mail import EmailMessage

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

                payment = Payment.objects.create(
                    original_amount = game.price,
                    discounted_amount = game.calculate_discounted_amount(rewards_used),
                    billing_method = request.POST['billing_method']
                )
                purchase = Purchase.objects.create(
                    member = member,
                    game = game,
                    payment = payment
                )
                
                member.use_rewards(rewards_used, purchase)
                email = EmailMessage('Purchase Confirmation',
                                     'Dear ' + request.user.username + ',\n' + 'Thank you for purchasing ' + purchase.game.name + '!',
                                     to=[request.user.email])
                email.send()
                purchase.issue_rewards(member)

    return redirect(reverse('games:game', kwargs={'id': gameID}))