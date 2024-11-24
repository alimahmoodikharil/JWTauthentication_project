from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework import status
import datetime
import jwt
from .serializers import CustomUserSerializer
from .models import CustomUser



class SignUpView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

class SignInView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email = email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if token is None:
            raise NotAuthenticated('Not Authenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Singin Session Expired!')
        
        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'Status': 'Successful'
        }
        return response