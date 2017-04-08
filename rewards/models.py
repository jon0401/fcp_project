from django.db import models

from datetime import datetime
from datetime import timedelta

# Create your models here.
class Reward(models.Model):
    award_datetime = models.DateTimeField(default=datetime.now())
    expiry_datetime = models.DateTimeField(default=datetime.now() + timedelta(days=120))
    member = models.ForeignKey("users.Member")
    purchase = models.ForeignKey("purchases.Purchase", blank=True, null=True)