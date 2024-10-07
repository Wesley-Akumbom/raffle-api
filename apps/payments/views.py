import uuid

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer

from .utils.flutterwave_client import FlutterwaveClient
from ..ticketHolders.models import TicketHolders
from ..tickets.models import Ticket


class PaymentView(APIView):
    def post(self, request):
        try:
            ticket_id = request.data['ticket_id']
            phone_number = request.data['phone_number']

            user = request.user
            fullname = user.username

            # Fetch the ticket using the provided ticket_id
            ticket = Ticket.objects.get(id=ticket_id)

            flutterwave_client = FlutterwaveClient()
            tx_ref = str(uuid.uuid4())  # Generate a unique transaction reference

            # Initiate mobile money payment request
            payment_request = flutterwave_client.initiate_mobile_money_payment(
                amount=float(ticket.price),
                phone_number=phone_number,
                tx_ref=tx_ref,
                fullname=fullname
            )

            # Log the payment request response
            print("Payment request response:", payment_request)

            # Create the payment record
            payment = Payment.objects.create(
                user=request.user,
                ticket=ticket,
                payment_method='mobilemoney',
                payment_amount=ticket.price,
                currency='XAF',
                flutterwave_transaction_id=tx_ref,
                flutterwave_transaction_status=payment_request.get('status', 'UNKNOWN')
            )

            # Check if the transaction status is 'successful' to create TicketHolders instance
            if payment.flutterwave_transaction_status == 'success':
                TicketHolders.objects.create(
                    user=payment.user,
                    ticket=payment.ticket,
                    purchase_date=payment.payment_date  # Use payment date for record keeping
                )

            serializer = PaymentSerializer(payment)

            return Response({
                'payment': serializer.data,
                'flutterwave_transaction_id': tx_ref  # Return the transaction reference
            }, status=status.HTTP_202_ACCEPTED)

        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckPaymentStatusView(APIView):
    def get(self, request, transaction_id):
        try:
            payment = Payment.objects.get(flutterwave_transaction_id=transaction_id)  # Ensure the correct field is used
            flutterwave_client = FlutterwaveClient()

            status_response = flutterwave_client.check_transaction_status(transaction_id)

            payment.flutterwave_transaction_status = status_response.get('status',
                                                                         'UNKNOWN')  # Update transaction status
            if status_response.get('status') == 'successful':
                TicketHolders.objects.create(
                    user=payment.user,
                    ticket=payment.ticket,
                    purchase_date=payment.payment_date
                )
            elif status_response.get('status') == 'failed':
                # Handle failed payments if needed
                pass

            payment.save()

            serializer = PaymentSerializer(payment)
            return Response(serializer.data)

        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class MoMoCallbackView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            transaction_id = data.get('referenceId')  # Adjust based on actual payload structure
            status = data.get('status')

            payment = Payment.objects.get(flutterwave_transaction_id=transaction_id)  # Ensure the correct field is used
            payment.flutterwave_transaction_status = status  # Update transaction status

            if status == 'SUCCESSFUL':
                TicketHolders.objects.create(
                    user=payment.user,
                    ticket=payment.ticket,
                    purchase_date=payment.payment_date  # Use payment date for record keeping
                )
            elif status == 'FAILED':
                # Handle failed payments if needed
                pass

            payment.save()

            return Response({'message': 'Callback processed successfully'}, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            print(f"Payment with transaction ID {transaction_id} not found.")
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in MoMo callback: {str(e)}")  # Log the error for debugging purposes
            return Response({'error': 'Failed to process callback'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
