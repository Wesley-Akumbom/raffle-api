from rest_framework import serializers
from .models import TicketHolders


class TicketUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketHolders
        fields = ['id', 'user', 'ticket', 'purchase_date']
