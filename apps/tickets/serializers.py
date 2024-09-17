from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    ticket_name = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_name', 'price', 'raffle']
