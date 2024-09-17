from django.db import models
from apps.core.models import BaseModel
from apps.raffles.models import Raffle


class Ticket(BaseModel):
    class TicketManager(models.Manager):
        pass

    ticket_name = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    raffle = models.OneToOneField(Raffle, on_delete=models.CASCADE)

    objects = TicketManager()

    def save(self, *args, **kwargs):
        if not self.ticket_name:
            self.ticket_name = self.generate_ticket_name()
        super().save(*args, **kwargs)

    def generate_ticket_name(self):
        # Get the first letter of the raffle name
        if self.raffle and self.raffle.name:
            first_letter = self.raffle.name[0].upper()  # Get the first letter and convert to uppercase
        else:
            first_letter = 'R'  # Default letter if no raffle is associated

        # Get the last ticket number from the database for this raffle
        last_ticket = Ticket.objects.filter().order_by('id').last()
        if last_ticket:
            last_number = int(last_ticket.ticket_name[4:])  # Extract the number from the last ticket name
            new_number = last_number + 1
        else:
            new_number = 1  # Start from 1 if no tickets exist for this raffle

        # Generate the new ticket name in the format "TSA{first_letter}{number}"
        return f"TSA{first_letter}{new_number:03d}"  # Format the number to be three digits (e.g., 001, 002)

    def __str__(self):
        return self.ticket_name
