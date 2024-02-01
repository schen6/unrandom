from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email')  # Add other fields if necessary
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Check if the username or email already exists
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'A user with that username already exists.'})
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'A user with that email already exists.'})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user