from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment, PaymentStatus
from .serializers import PaymentSerializer
import stripe
from django.conf import settings

from ..tickets.models import Ticket

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class PaymentView(APIView):
    def post(self, request):
        try:
            ticket_id = request.data['ticket_id']
            payment_method_id = request.data['payment_method_id']  # Get the payment method ID from the request

            # Retrieve the ticket object from the database
            ticket = Ticket.objects.get(id=ticket_id)

            # Create a new payment intent with the payment method ID
            payment_intent = stripe.PaymentIntent.create(
                amount=int(ticket.price * 100),  # Convert to cents
                currency='usd',
                payment_method=payment_method_id,
                confirm=True,  # Automatically confirm the payment intent
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never'  # Disable redirects for automatic payments
                }
            )

            # Create a new payment object in your database
            payment = Payment.objects.create(
                user=request.user,
                ticket=ticket,
                payment_method='card',  # Indicate that the payment method is a card
                payment_status=PaymentStatus.SUCCEEDED if payment_intent.status == 'succeeded' else PaymentStatus.FAILED,
                payment_amount=ticket.price,
                currency='usd',
                stripe_payment_intent_id=payment_intent.id,
            )

            serializer = PaymentSerializer(payment)

            return Response({
                'payment': serializer.data,
            }, status=status.HTTP_201_CREATED)

        except stripe.error.CardError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_TEST_SECRET_KEY  # Use your webhook secret here
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Get the payment intent ID from the event data
        payment_intent_id = event['data']['object']['id']

        # Get the payment object
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the payment status based on the event type
        if event['type'] == 'payment_intent.succeeded':
            payment.payment_status = PaymentStatus.SUCCEEDED
        elif event['type'] == 'payment_intent.payment_failed':
            payment.payment_status = PaymentStatus.FAILED

        # Save the updated payment object
        payment.save()

        return Response({'message': 'Payment updated successfully'})