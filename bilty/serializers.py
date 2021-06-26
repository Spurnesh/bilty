from rest_framework import serializers
from core.models import Bilty, User


class BiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilty
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "user_password",
            "phone",
            "address",
        ]