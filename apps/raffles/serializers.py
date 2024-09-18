from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Raffle


class RaffleSerializer(ModelSerializer):
    ticket_id = serializers.PrimaryKeyRelatedField(source='ticket', read_only=True)

    class Meta:
        model = Raffle
        fields = ['id', 'ticket_id', 'name', 'num_winners', 'prize_name', 'prize_img']
