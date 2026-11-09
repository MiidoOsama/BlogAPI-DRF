from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer,RegisterSerializer



class RegisterView(APIView):
    permission_classes= [AllowAny] 
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message":"User Created Succesffully!",
            "user":serializer.data,
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        })

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            refresh_token=request.data.get('refresh')
            if not refresh_token:
                return Response({'error':'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'Successfully logged out'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':'invalid token'},status=status.HTTP_400_BAD_REQUEST)
        