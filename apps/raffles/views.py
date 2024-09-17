from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.raffles.models import Raffle
from apps.raffles.serializers import RaffleSerializer


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
