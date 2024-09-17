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
