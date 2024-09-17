from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.tickets.models import Ticket, Raffle
from apps.tickets.serializers import TicketSerializer


class TicketListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        raffle_id = request.data.get('raffle_id')
        try:
            raffle = Raffle.objects.get(id=raffle_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Raffle not found'}, status=status.HTTP_404_NOT_FOUND)

        ticket_data = {
            'price': request.data.get('price'),
            'raffle': raffle.id
        }

        serializer = TicketSerializer(data=ticket_data)

        if serializer.is_valid():
            ticket = serializer.save()  # Automatically generates ticket_name in save method
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket)
        return Response(serializer.data)


class TicketUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a partial serializer that only allows updating the price field
        price_data = {'price': request.data.get('price')}

        # Use a serializer that only includes the price field for updates
        serializer = TicketSerializer(ticket, data=price_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id):
        try:
            ticket = Ticket.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        ticket.delete()
        return Response({'message': 'Ticket deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
