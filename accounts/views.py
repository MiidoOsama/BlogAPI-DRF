from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer



class RegisterView(APIView):
    permission_classes= [AllowAny]


    def post(self,request):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')

        if not username or not email or not password :
            return Response({'error':'All fields are required!'},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error':'username already exist'},status=status.HTTP_400_BAD_REQUEST)


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        serializer = UserSerializer(user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message':'User created successfully!',
            'user': serializer.data,
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        },status=status.HTTP_201_CREATED)