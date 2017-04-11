from django.db import models

from datetime import datetime

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    detailed_description = models.CharField(max_length = 2000)
    platforms = models.ManyToManyField("platforms.Platform")
    genre = models.ForeignKey("genres.Genre")
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    tags = models.ManyToManyField("tags.Tag")
    release_datetime = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to='images/', default='/static/defaultGame.png')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name