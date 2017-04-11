from django.db import models

from datetime import *
from django.utils import timezone

from .helpers import *

# Create your models here.
class Reward(models.Model):
    award_datetime = models.DateTimeField(default=timezone.now, blank=True)
    expiry_datetime = models.DateTimeField(default=calculate_expiry_datetime, blank=True)
    member = models.ForeignKey("users.Member")
    purchase = models.ForeignKey("purchases.Purchase", blank=True, null=True)

    def __str__(self):
        if(self.purchase is None):
            return str(self.award_datetime)
        else:
            return str(self.award_datetime) + ' ****USED'

    def isExpired(self):
        if(timezone.now() >= self.expiry_datetime):
            return True

    class Meta(object):
        ordering = ('award_datetime',)