from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['username','email']


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields=['username','email','password']

    def create(slef,validated_data):
        return User.objects.create_user(**validated_data)