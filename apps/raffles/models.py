from django.db import models
from django.db.models.manager import BaseManager

from apps.core.models import BaseModel


class Raffle(BaseModel):
    class RaffleManager(models.Manager):
        pass

    name = models.CharField(max_length=255)
    num_winners = models.PositiveIntegerField()

    objects = RaffleManager()

    def __str__(self):
        return self.name
