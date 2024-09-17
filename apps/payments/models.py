from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User
from apps.tickets.models import Ticket


class PaymentStatus(models.TextChoices):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'


class Payment(BaseModel):

    class PaymentManager(models.Manager):
        pass

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent_id = models.CharField(max_length=50, blank=True, null=True)

    objects = PaymentManager()

    def __str__(self):
        return f"Payment for {self.ticket.ticket_name}"
