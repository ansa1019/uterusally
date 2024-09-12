from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import pre_save
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from chat.models import Chat
from content.models import TextEditorPost, TextEditorPostComment
from .serializer import *
from .models import *

# Create your views here.


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def list(self, request, *args, **kwargs):
        queryset = Status.objects.all().order_by("id")
        status = {}

        for query in queryset:
            status[query.name] = query.id
        return Response(status)


class blacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if "chat" in request.data:
            chat = Chat.objects.get(id=request.data["chat"])
            bl = Blacklist.objects.create(
                user=user, blacklist=chat.user, chat=chat, reason=request.data["reason"]
            )
        elif "post" in request.data:
            post = TextEditorPost.objects.get(id=request.data["post"])
            bl = Blacklist.objects.create(
                user=user,
                blacklist=post.author,
                post=post,
                reason=request.data["reason"],
            )
        else:
            comment = TextEditorPostComment.objects.get(id=request.data["comment"])
            bl = Blacklist.objects.create(
                user=user,
                blacklist=comment.author,
                comment=comment,
                reason=request.data["reason"],
            )
        bl.save()
        return Response({"status": "blacklist success"})

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})
        elif not self.request.user.is_staff:
            return Response({"error": "user is not staff"})
        else:
            user = request.user
            queryset = Blacklist.objects.all().order_by("status", "created_at")
            blacklist = []

            for query in queryset:
                user = User.objects.get(id=query.user.id)
                bluser = User.objects.get(id=query.blacklist.id)

                if query.post is not None:
                    category = "文章"
                    content = query.post.title
                    url = (
                        "TreatmentArticleGet/" + str(query.post.id) + "/"
                        if "聊療" in query.post.category.all()[0].name
                        else "knowledge_article/" + str(query.post.id) + "/"
                    )
                elif query.comment is not None:
                    category = "留言"
                    content = query.comment.body
                    url = (
                        "TreatmentArticleGet/"
                        + str(query.comment.post.id)
                        + "#comment_"
                        + str(query.comment.id)
                        if "聊療" in query.comment.post.category.all()[0].name
                        else "knowledge_article/"
                        + str(query.comment.post.id)
                        + "#comment_"
                        + str(query.comment.id)
                    )
                else:
                    category = "聊天室"
                    content = query.chat.message
                    url = "/#chat_" + str(query.chat.id)

                blacklist.append(
                    {
                        "id": query.id,
                        "category": category,
                        "content": content,
                        "user": user.username,
                        "blacklist": bluser.username,
                        "reason": query.reason,
                        "created_at": query.created_at,
                        "status": query.status.name,
                        "url": url,
                    }
                )
            return Response(blacklist)


class getBlacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user

        queryset = self.queryset.filter(user=user)
        blacklist = {"article": [], "comment": [], "chat": []}

        for query in queryset:
            if query.post is not None:
                blacklist["article"].append(query.post.id)
            elif query.comment is not None:
                blacklist["comment"].append(query.comment.id)
            elif query.chat is not None:
                blacklist["chat"].append(query.chat.id)
        return Response(blacklist)


class getBanlistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Ban.objects.filter(
            Q(blacklist__blacklist=user)
            & (Q(end_time__gt=timezone.now()) | Q(end_time__isnull=True))
        )
        res = {"article": True, "comment": True, "chat": True}

        if queryset.count() > 0:
            for query in queryset:
                bl = query.blacklist
                if bl.post is not None:
                    res["article"] = [bl.status.name, query.start_time]
                elif bl.comment is not None:
                    res["comment"] = [bl.status.name, query.start_time]
                elif bl.chat is not None:
                    res["chat"] = [bl.status.name, query.start_time]
        return Response(res)