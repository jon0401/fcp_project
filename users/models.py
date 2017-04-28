from django.db import models
from django.contrib.auth.models import User
from rewards.models import Reward
from games.models import Game

from datetime import *
from django.utils import timezone


# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length = 200)
    reserved_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    games = models.ManyToManyField("games.Game", through="purchases.Purchase", blank=True)
    avatar = models.ImageField(default=0, blank=True)

    def __str__(self):
        return self.user.username

    def use_rewards(self, quantity, purchase):
        if(quantity > 10):
            quantity = 10
      
        rewards = Reward.objects.filter(member=self, purchase__isnull=True, expiry_datetime__gt=timezone.now()).order_by('expiry_datetime')[:quantity]
        for reward in rewards:
            reward.purchase = purchase
            reward.save()

    def get_recommended_games(self):
        target_purchases = self.purchase_set.all().order_by('datetime')[:3]

        target_games = [p.game for p in target_purchases]
        non_target_games = [g for g in Game.objects.all() if g not in target_games]
        recommended_games = []

        for tg in target_games:
            tags_shared_max_count = max([len(set(tg.tags.all()).intersection(ntg.tags.all())) for ntg in non_target_games])
            best_matches = [ntg for ntg in non_target_games if len(set(tg.tags.all()).intersection(ntg.tags.all())) == tags_shared_max_count]
            best_matches.sort(key=lambda g: g.release_datetime, reverse=True)
      
            recommended_games.append(best_matches[0])

        return list(set(recommended_games))

    def has_purchased(self, game):
        purchases = self.purchase_set.all()
        purchased_games = [purchase.game for purchase in purchases]

        if game in purchased_games:
            return True
        else:
            return False

    def remove_expired_rewards(self):
        rewards = self.reward_set.all()
        for reward in rewards:
            if reward.isExpired():
                reward.delete()

    def calculate_spending_required_for_next_reward(self):
        return 100 - self.reserved_amount
