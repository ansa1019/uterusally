from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from content.models import TextEditorPost, TextEditorPostComment
from userprofile.models import profile, subscribeHashtag
from blacklist.models import Blacklist
from point.models import *
from .models import *
from .serializer import *

# Create your views here.


class notificationsView(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = notificationsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if "author" in request.data:
            post = TextEditorPost.objects.get(id=request.data["author"])
            comments = TextEditorPostComment.objects.filter(post=post)
            try:
                notify, created = Notifications.objects.get_or_create(
                    user=post.author, post=post
                )
                notify.content = (
                    request.data["content"]
                    .replace("#", post.title, 1)
                    .replace("#", str(post.like.count()), 1)
                    .replace("#", str(comments.count()), 1)
                    .replace("#", str(post.share.count()), 1)
                )
                notify.created_at = timezone.now()
                notify.read = False
                notify.save()
            except Exception as e:
                print(e)
        elif "post" in request.data:
            post = TextEditorPost.objects.get(id=request.data["post"])
            if "content_subscribe" in request.data:
                subscribes = profile.objects.filter(subscribe__in=[user])
                for sub in subscribes:
                    try:
                        notify, created = Notifications.objects.get_or_create(
                            user=sub.user, author=post.author
                        )
                        notify.content = request.data["content_subscribe"]
                        notify.created_at = timezone.now()
                        notify.read = False
                        notify.save()
                    except Exception as e:
                        print(e)
            if post.hashtag:
                hashtags = post.hashtag.split(",")
                for tag in hashtags:
                    try:
                        subscribes = subscribeHashtag.objects.filter(hashtag=tag)
                        for sub in subscribes:
                            try:
                                notify, created = Notifications.objects.get_or_create(
                                    user=sub.user, hashtag=sub
                                )
                                notify.content = request.data["content_hashtag"].replace(
                                    "#", tag, 1
                                )
                                notify.created_at = timezone.now()
                                notify.read = False
                                notify.save()
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
        elif "gift" in request.data:
            gif = gift.objects.get(id=request.data["gift"])
            poi = point.objects.get(user=user)
            poi2 = point.objects.get(user=gif.receiver)
            try:
                # giver
                notify, created = Notifications.objects.get_or_create(
                    user=user, gift=gif
                )
                notify.content = (
                    request.data["content"]
                    .replace("#", gif.receiver.username, 1)
                    .replace("#", str(gif.point), 1)
                    .replace("#", str(poi.point), 1)
                )
                notify.created_at = timezone.now()
                notify.read = False
                notify.save()

                # receiver
                notify2, created2 = Notifications.objects.get_or_create(
                    user=gif.receiver, gift=gif
                )
                notify2.content = (
                    request.data["content2"]
                    .replace("#", gif.giver.username, 1)
                    .replace("#", str(gif.point), 1)
                    .replace("#", str(poi2.point), 1)
                )
                notify2.created_at = timezone.now()
                notify2.read = False
                notify2.save()
            except Exception as e:
                print(e)
        elif "exchange" in request.data:
            try:
                text = request.data["first_content"]
                points = 0
                exc = exchange.objects.get(id=request.data["exchange"])
                for item in exchangeProducts.objects.filter(exchange=exc):
                    points += item.point
                    text += (
                        request.data["products_content"]
                        .replace("#", str(item.amount), 1)
                        .replace("#", item.product.product_title, 1)
                        + "、"
                    )
                poi = point.objects.get(user=user)
                text = text[:-1] + request.data["point_content"].replace(
                    "#", str(points), 1
                ).replace("#", str(poi.point), 1)

                notify = Notifications.objects.create(
                    user=user,
                    exchange=exc,
                    content=text,
                    created_at=timezone.now(),
                    read=False,
                )
                serializer = self.serializer_class(notify)
                return Response(serializer.data)
            except Exception as e:
                print(e)
                return Response({"error": e})
        elif "blacklist" in request.data:
            blacklist = Blacklist.objects.get(id=request.data["blacklist"])
            try:
                notify, created = Notifications.objects.get_or_create(
                    user=blacklist.blacklist,
                    blacklist=blacklist,
                )
                notify.content = request.data["content"]
                notify.created_at = timezone.now()
                notify.read = False
                notify.save()
            except Exception as e:
                print(e)
        # 目前前端沒有新增產品的功能，有的話再加
        # elif "product" in request.data:
        #     pro = product.objects.get(id=request.data["product"])
        #     try:
        #         notify, created = Notifications.objects.get_or_create(
        #             user=user, product=pro
        #         )
        #         notify.content = request.data["content"]
        #         notify.created_at = timezone.now()
        #         notify.read = False
        #         notify.save()
        #     except Exception as e:
        #         print(e)
        serializer = self.serializer_class(
            notify, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def list(self, request, *args, **kwargs):
        # if self.request.user.is_anonymous:
        #     return Response({"error": "user is anonymous"})
        # else:
        user = self.request.user
        queryset = Notifications.objects.filter(user=user).order_by(
            "-read", "-created_at"
        )

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class getNotificationsView(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = notificationsSerializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})
        else:
            user = self.request.user
            queryset = Notifications.objects.filter(user=user, read=False).order_by(
                "-created_at"
            )

            serializer = self.serializer_class(
                queryset, many=True, context={"request": request}
            )
        return Response(serializer.data)
