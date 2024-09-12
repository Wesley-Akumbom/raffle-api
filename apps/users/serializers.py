from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
        }

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])  # Set hashed password
        user.save()  # Save user to the database
        return user
