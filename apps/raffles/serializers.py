from rest_framework.serializers import ModelSerializer
from .models import Raffle


class RaffleSerializer(ModelSerializer):
    class Meta:
        model = Raffle
        fields = ['id', 'name', 'num_winners', 'prize_name', 'prize_img']
