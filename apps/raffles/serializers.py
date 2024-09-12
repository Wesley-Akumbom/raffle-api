from rest_framework.serializers import ModelSerializer
from .models import Raffle


class RaffleSerializer(ModelSerializer):
    class Meta:
        model = Raffle
        fields = '__all__'
