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
    check = models.BooleanField(default=False)

    def __str__(self):
        if(self.purchase is None):
            return str(self.award_datetime)
        else:
            return str(self.award_datetime) + ' ****USED'

    def checking(self):
        if(self.expiry_datetime <= timezone.now()):
            self.check = True
        self.save()

    class Meta(object):
        ordering = ('award_datetime',)