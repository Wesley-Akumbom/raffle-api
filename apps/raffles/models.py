from django.db import models
from django.db.models.manager import BaseManager

from apps.core.models import BaseModel
from apps.users.models import User


class Raffle(BaseModel):
    class RaffleManager(models.Manager):
        pass

    name = models.CharField(max_length=255)
    prize_name = models.CharField(max_length=255)
    prize_img = models.ImageField(upload_to='images')
    num_winners = models.PositiveIntegerField()
    participants = models.ManyToManyField(User, related_name='raffles', blank=True)

    objects = RaffleManager()

    def __str__(self):
        return self.name
