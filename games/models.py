from django.db import models

from datetime import *
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    detailed_description = models.CharField(max_length = 2000)
    platforms = models.ManyToManyField("platforms.Platform")
    genre = models.ForeignKey("genres.Genre")
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    tags = models.ManyToManyField("tags.Tag")
    release_datetime = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images/', default='/static/defaultGame.png')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def calculate_discounted_amount(self, rewards_used):
        discounted_amount = (Decimal(1) - (Decimal(0.1) * rewards_used)) * self.price

        if(discounted_amount > Decimal(0)):
            return discounted_amount
        else:
            return Decimal(0)