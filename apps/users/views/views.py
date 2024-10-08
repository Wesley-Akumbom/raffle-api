from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def put(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is trying to update their own account
        if request.user.id != user.id:
            return Response({'error': 'You do not have permission to update this user.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def delete(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)