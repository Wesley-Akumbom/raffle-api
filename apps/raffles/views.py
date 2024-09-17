from random import choice

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.raffles.models import Raffle
from apps.raffles.serializers import RaffleSerializer
from apps.ticketHolders.models import TicketHolders
from apps.winners.models import Winners


class RaffleCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = RaffleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RaffleUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, id):
        raffle = Raffle.objects.get(id=id)
        serializer = RaffleSerializer(raffle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RaffleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raffles = Raffle.objects.all()
        serializer = RaffleSerializer(raffles, many=True)
        return Response(serializer.data)


class RaffleDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, id):
        try:
            return Raffle.objects.get(id=id)
        except Raffle.DoesNotExist:
            return None

    def get(self, request, id):
        raffle = self.get_object(id)
        if raffle is None:
            return Response({'error': 'Raffle not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RaffleSerializer(raffle)
        return Response(serializer.data)


class RaffleDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, id):
        try:
            return Raffle.objects.get(id=id)
        except Raffle.DoesNotExist:
            return None

    def delete(self, request, id):
        raffle = self.get_object(id)
        if raffle is None:
            return Response({'error': 'Raffle not found'}, status=status.HTTP_404_NOT_FOUND)

        raffle.delete()
        return Response({'message': 'Raffle deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class RunRaffleView(APIView):
    def post(self, request, raffle_id):
        try:
            # Retrieve the raffle
            raffle = Raffle.objects.get(id=raffle_id)

            # Retrieve all ticket holders for the specified raffle
            ticket_users = TicketHolders.objects.filter(ticket__raffle_id=raffle_id)

            # Check how many winners have already been created for this raffle
            current_winner_count = Winners.objects.filter(ticket_user__ticket__raffle=raffle).count()

            if current_winner_count >= raffle.num_winners:
                return Response({'error': 'This raffle has already produced the maximum number of winners.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not ticket_users.exists():
                return Response({'error': 'No ticket holders found for this raffle.'}, status=status.HTTP_404_NOT_FOUND)

            # Select a random ticket holder as the winner
            winner_ticket_user = choice(ticket_users)

            # Create a new Winner object
            winner = Winners.objects.create(ticket_user=winner_ticket_user)

            # Prepare response data
            response_data = {
                'username': winner_ticket_user.user.username,
                'raffle_name': winner_ticket_user.ticket.raffle.name,
                'prize': winner_ticket_user.ticket.raffle.prize_name,
                'ticket_name': winner_ticket_user.ticket.ticket_name,
                'winner_id': winner.id,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Raffle not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)