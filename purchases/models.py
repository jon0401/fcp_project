from django.db import models

from datetime import *
from django.utils import timezone

# Create your models here.
class Purchase(models.Model):
    member = models.ForeignKey("users.Member")
    game = models.ForeignKey("games.Game")
    datetime = models.DateTimeField(default=timezone.now)
    original_amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    discounted_amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    billing_method = models.CharField(max_length = 200)

    def __str__(self):
        return self.game.name + ' - ' + str(self.datetime)

    def issue_rewards(self, member):
        temp = member.reserved_amount + self.discounted_amount

        while (temp >= 100):
            temp -= 100
            member.reward_set.create(member=member)

        member.reserved_amount = temp
        member.save()