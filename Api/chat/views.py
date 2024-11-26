from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from blacklist.models import Blacklist
from .serializer import *
from .models import *

# Create your views here.


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        chat = Chat.objects.create(
            room=data["room"],
            user=User.objects.get(username=request.user.username),
            identity=data["identity"],
            message=data["message"],
        )
        return Response(
            {
                "id": chat.id,
                "message": "新增對話成功",
            },
            status=status.HTTP_201_CREATED,
        )


class getUserViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def list(self, request, *args, **kwargs):
        query = self.queryset.filter(id=request.GET.get("id"))
        id = query.values("user")[0]["user"]
        user = User.objects.get(id=id)
        return Response(user.username)


class getPreviousViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = previousChatSerializer

    def list(self, request, *args, **kwargs):
        blacklist = Blacklist.objects.filter(
            user=self.request.user, chat__isnull=False)
        if blacklist != []:
            query = (
                self.queryset.filter(room=request.GET.get("room"))
                .exclude(desable=True)
                .exclude(user__in=blacklist.values("blacklist"))
                .order_by("-id")[:20]
            )
        else:
            query = (
                self.queryset.filter(room=request.GET.get("room"))
                .exclude(desable=True)
                .order_by("-id")[:20]
            )

        serializer = self.serializer_class(
            query, many=True, context={"request": request}
        )
        return Response(serializer.data)
