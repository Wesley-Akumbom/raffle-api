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
