from django.db import models
from datetime import *
from django.utils import timezone

# Create your models here.
class Reward(models.Model):
    award_datetime = models.DateTimeField(default=datetime.today, blank=True)
    expiry_datetime = models.DateTimeField(default=datetime.today, blank=True)
    member = models.ForeignKey("users.Member")
    purchase = models.ForeignKey("purchases.Purchase", blank=True, null=True)
    check = models.BooleanField(default=False)

    def __str__(self):
        if (self.purchase is None):
            return str(self.award_datetime)
        else:
            return str(self.award_datetime) + ' ****USED'

    def checking(self):
        self.expiry_datetime = self.award_datetime + timedelta(days=120)
        if (self.expiry_datetime <= timezone.now()):
            self.check = True
        self.save()

    class Meta(object):
        ordering = ('award_datetime',)


