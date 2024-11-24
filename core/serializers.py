from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.urls import reverse


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




class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            CustomUser.objects.get(email=value)
        
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('There is no user with this email')
        
        return value
    
    def send_reset_password_email(self, user):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url_name = reverse('reset_password', kwargs={'uid': uid, 'token': token})
        url = f"http://127.0.0.1:8000{url_name}"

        send_mail(
            subject= 'Reset Password',
            message= f'Please click the link below to start the process: \n {url}',
            from_email= 'Ali@domain.com',
            recipient_list=[user.email]
        )
    
    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        self.send_reset_password_email(user)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        uid = self.context.get('uid')
        token = self.context.get('token')

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk= user_id)
        
        except (ValueError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Invalid user id!')
        
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError('Invalid info...')
        
        return {'user': user, 'new_password': data['new_password']}
    
    def save(self):
        validated_data = self.validated_data
        user = validated_data['user']

        user.set_password(validated_data['new_password'])
        user.save()
