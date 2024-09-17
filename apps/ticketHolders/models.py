from django.db import models
from apps.users.models import User
from apps.tickets.models import Ticket
from apps.payments.models import Payment


class TicketHolders(models.Model):
    class TicketManager(models.Manager):
        pass

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField()

    objects = TicketManager()

    def __str__(self):
        return f"{self.user.username} - {self.ticket.ticket_name}"
