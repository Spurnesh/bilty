from django.shortcuts import render
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from bilty.serializers import *

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class LoginAuth(ObtainJSONWebToken):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if user:
            if check_password(data['password'], user.password):
                credentials = {
                    'username': user.email,
                    'password': data['password']
                }
                user = authenticate(request, username=data['username'],
                                    password=data['password'])
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                return Response({
                    "status": True,
                    "token": token
                    },
                    status=status.HTTP_200_OK
                )
            return Response({
                "status": False,
                "message": "please enter valid password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            "status": False,
            "message": "Username not exist"},
            status=status.HTTP_400_BAD_REQUEST
        )


class BiltyView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BiltySerializer

    def post(self, request):
        user = request.user
        request.data.update({"user": user.id})
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Bilty added successfully",
                "data": serializer.data
            },
                status=status.HTTP_201_CREATED)
        return Response({
            "message": "some fields is required ",
            "data": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.user.is_superuser:
            bilty = Bilty.objects.all()
        else:
            bilty = Bilty.objects.filter(user=request.user)
        serializer = self.serializer_class(bilty, many=True)
        return Response({
            "total_records": bilty.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def post(self, request):
        user = request.user
        if user.is_superuser:
            request.data.update({"user": user.id, 'user_password': request.data['password']})
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                obj.set_password(request.data['password'])
                obj.save()
                return Response({
                    "message": "User added successfully",
                },
                    status=status.HTTP_201_CREATED)
            return Response({
                "message": "some fields is required ",
                "data": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "This user not access for this modules",
        },
            status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetUserSerializer

    def get(self, request):
        if request.user.is_superuser:
            user = User.objects.all()
            serializer = self.serializer_class(user, many=True)
            return Response({
                "total_records": user.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "This user not access for this modules",
        },
        status=status.HTTP_400_BAD_REQUEST)
