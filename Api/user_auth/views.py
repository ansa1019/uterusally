from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from datetime import timedelta
from django.utils import timezone
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
        from userdetail.models import forgetPassword

        try:
            user = User.objects.get(username=username)
            record = forgetPassword.objects.create(
                user=user, verification_code=request.data["verification_code"]
            )
            return Response({"result": "success"})
        except Exception as e:
            print(e)
            return Response({"result": "error"})


class UpdatePasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, username):
        if self.request.user.is_anonymous:
            from userdetail.models import forgetPassword

            try:
                now = timezone.now()
                before = now - timedelta(minutes=5)
                user = User.objects.get(username=username)
                verification_code = request.data["verification_code"]
                record = forgetPassword.objects.filter(
                    user=user, created_at__range=[before, now]
                ).order_by("-created_at")[0]
                if verification_code == record.verification_code:
                    user.set_password(request.data["password"])
                    user.save()
                    return Response({"result": "success"})
                else:
                    return Response({"result": "error", "error": "verification code"})
            except Exception as e:
                print(e)
                return Response({"error": "error"})
        else:
            try:
                user = User.objects.get(username=username)
                user.set_password(request.data["password"])
                user.save()
                return Response({"result": "success"})
            except Exception as e:
                print(e)
                return Response({"result": "error"})
