from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

# Create your views here.
from rest_framework_simplejwt.serializers import TokenVerifySerializer


"""
之後的信箱驗證會用到這個
"""


class RegisterationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterationSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        # print(self.request.user.username)
        return User.objects.filter(username=self.request.user.username)


class MailVerifyViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VerifySerializer
    permission_classes = (AllowAny,)

    def list(self, request, username):
        res = User.objects.filter(username=username).count() > 0
        return Response({"result": res})


class ForgetPasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, username):
        try:
            user = User.objects.get(username=username)
            user.set_password(request.data["password"])
            user.save()
            return Response({"result": "success"})
        except:
            return Response({"result": "error"})
