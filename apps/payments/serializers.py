from datetime import datetime

from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'ticket', 'payment_method', 'payment_status', 'payment_amount',
                  'currency', 'payment_date', 'stripe_payment_intent_id']

    def get_payment_method(self, obj):
        # Return a fixed test card number
        return "4242 4242 4242 4242"


def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")


def check_expiry_year(value):
    today = datetime.now().year
    if not int(value) >= today:
        raise serializers.ValidationError("Invalid expiry year.")


def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid CVC number.")


class PaymentMethodSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, required=True)
    expiry_month = serializers.CharField(max_length=2, required=True, validators=[check_expiry_month])
    expiry_year = serializers.CharField(max_length=4, required=True, validators=[check_expiry_year])
    cvc = serializers.CharField(max_length=4, required=True, validators=[check_cvc])
