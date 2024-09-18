from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import TicketHolders
from .serializers import TicketUsersSerializer


class TicketHoldersListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        ticketUsers = TicketHolders.objects.all()
        serializer = TicketUsersSerializer(ticketUsers, many=True)
        return Response(serializer.data)


class TicketHoldersDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            # Fetch all ticket holders associated with the given user ID
            ticket_holders = TicketHolders.objects.filter(user_id=user_id)
            if not ticket_holders.exists():
                return Response('You have no tickets', status=status.HTTP_404_NOT_FOUND)

            serializer = TicketUsersSerializer(ticket_holders, many=True)  # Serialize all instances
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)