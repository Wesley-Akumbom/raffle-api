from datetime import datetime
from rest_framework import serializers
from .models import Payment

from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'ticket',
            'payment_method',
            'payment_amount',
            'currency',
            'payment_date',
            'flutterwave_transaction_id',  # Use the correct field name
            'flutterwave_transaction_status'  # Use the correct field name
        ]

    def get_payment_method(self, obj):
        # Return the payment method as "Mobile Money" (or customize as needed)
        return "Mobile Money"


class PaymentMethodSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, required=True)  # Adjust max_length as necessary

    def validate_phone_number(self, value):
        # Add any specific validation for phone numbers if needed
        if len(value) < 9 or len(value) > 15:  # Example validation for Cameroon phone numbers
            raise serializers.ValidationError("Invalid phone number.")
        return value
