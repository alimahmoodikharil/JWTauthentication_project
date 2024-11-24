from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        if not password:
            raise serializers.ValidationError({'password': 'Password is required!'})
        
        user = CustomUser(**validated_data)
        user.password = make_password(password)  
        user.save()
        return user