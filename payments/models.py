from django.db import models

# Create your models here.
class Payment(models.Model):
    original_amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    discounted_amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    billing_method = models.CharField(max_length = 200)

    def __str__(self):
        return 'ID:' + str(self.id) + ' - $' + str(self.discounted_amount) + ' - ' + self.billing_method