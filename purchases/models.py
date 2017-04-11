from django.db import models

from decimal import Decimal
from datetime import datetime

# Create your models here.
class Purchase(models.Model):
    member = models.ForeignKey("users.Member")
    game = models.ForeignKey("games.Game")
    datetime = models.DateTimeField(default=datetime.now)
    original_amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    discounted_amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    billing_method = models.CharField(max_length = 200)

    def __str__(self):
        return self.game.name + ' - ' + str(self.datetime)

    def get_discounted_amount(original_amount, rewards_used):
        discounted_amount = (Decimal(1) - (Decimal(0.1) * rewards_used)) * original_amount

        if(discounted_amount > Decimal(0)):
            return discounted_amount
        else:
            return Decimal(0)