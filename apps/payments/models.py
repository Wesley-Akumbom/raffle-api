from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User
from apps.tickets.models import Ticket


class Payment(BaseModel):
    class PaymentManager(models.Manager):
        pass

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, default='flutterwave')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='XAF')  # Set XAF as the default currency for Cameroon
    payment_date = models.DateTimeField(auto_now_add=True)

    flutterwave_transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Store Flutterwave tx_ref
    flutterwave_transaction_status = models.CharField(max_length=50, blank=True, null=True)  # Store transaction status

    objects = PaymentManager()

    def __str__(self):
        return f"Payment for {self.ticket.ticket_name}"
