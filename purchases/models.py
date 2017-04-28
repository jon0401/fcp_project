from django.db import models
from payments.models import Payment

from datetime import *
from django.utils import timezone
from django.core.mail import EmailMessage

# Create your models here.
class Purchase(models.Model):
    member = models.ForeignKey("users.Member")
    game = models.ForeignKey("games.Game")
    datetime = models.DateTimeField(default=timezone.now)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.game.name + ' - ' + str(self.datetime)

    def issue_rewards(self, member):
        temp = member.reserved_amount + self.payment.discounted_amount

        while (temp >= 100):
            temp -= 100
            member.reward_set.create(member=member)
            email = EmailMessage('New Reward Point',
                                 'Thank you for your purhcase again! You gain one new reward point!',
                                 to=[member.user.email])
            email.send()

        member.reserved_amount = temp
        member.save()