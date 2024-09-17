from django.db import models
from apps.ticketHolders.models import TicketHolders


class Winners(models.Model):

    class WinnersManager(models.Manager):
        pass

    ticket_user = models.OneToOneField(TicketHolders, on_delete=models.CASCADE, related_name='winner')
    date_won = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    objects = WinnersManager()

    def __str__(self):
        return f"Winner: {self.ticket_user.user.username} for {self.ticket_user.ticket.ticket_name} - Prize: {self.ticket_user.ticket.raffle.prize_name}"
