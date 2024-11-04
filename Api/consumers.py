import json
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.templatetags.static import static
from django.db.models.signals import post_save
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from userprofile.models import profile
from content.models import TextEditorPost, record
from notifications.models import Notifications
from notifications.serializer import notificationsSerializer
from blacklist.models import *
from chat.models import Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            await self.accept()
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def createMsg(self, room, identity, message):
        # create message
        msg = Chat.objects.create(
            room=room,
            user=self.user,
            identity=identity,
            message=message,
        )
        msg.save()
        userProfile = profile.objects.get(user=self.user)
        if identity != "匿名":
            try:
                user_image = userProfile.user_image.url
            except:
                user_image = static(userProfile.gender + ".png")
        else:
            user_image = static(userProfile.gender + ".png")
        return msg.id, user_image

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room = text_data_json["room"]
        identity = text_data_json["identity"]
        message = text_data_json["message"]
        # Send message to room group
        id, user_image = await self.createMsg(room, identity, message)
        print(id, room, self.user.username, identity, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "id": id,
                "user": self.user.username,
                "room": room,
                "identity": identity,
                "message": message,
                "user_image": user_image,
            },
        )

    async def chat_message(self, event):
        id = event["id"]
        user = event["user"]
        room = event["room"]
        identity = event["identity"]
        message = event["message"]
        user_image = event["user_image"]
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "id": id,
                    "user": user,
                    "room": room,
                    "identity": identity,
                    "message": message,
                    "user_image": user_image,
                }
            )
        )


class RecordConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.article = self.scope["url_route"]["kwargs"]["article_id"]

        if self.user.is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        end = timezone.now()
        self.id = await self.record("", end)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        if action == "connect":
            start = timezone.now()
            self.id = await self.record(start, "")
            # print(self.id, "start:", start)
        else:
            self.id = await self.reconnect()

    @database_sync_to_async
    def record(self, start, end):
        article = TextEditorPost.objects.get(id=self.article)
        # create record
        if start != "":
            rec = record.objects.create(
                user=self.user,
                article=article,
                start=start,
            )
        else:
            rec = record.objects.get(id=self.id)
            rec.end = end
        rec.save()
        return rec.id

    @database_sync_to_async
    def reconnect(self):
        article = TextEditorPost.objects.get(id=self.article)

        rec = record.objects.filter(user=self.user, article=article).order_by("-id")[0]
        rec.end = None
        rec.save()
        return rec.id


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(
                "user_" + str(self.user.id), self.channel_name
            )
            print("user_" + str(self.user.id), " joined")
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "user_" + str(self.user.id), self.channel_name
        )

    @database_sync_to_async
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["action"] == "all_read":
            Notifications.objects.filter(user=self.user, read=False).update(read=True)
        else:
            Notifications.objects.filter(id=text_data_json["id"]).update(read=True)

    async def notification_save(self, event):
        notifications = event["notifications"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"notifications": notifications}))

    async def blacklist_save(self, event):
        blacklist = event["blacklist"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"blacklist": blacklist}))

    async def banlist_save(self, event):
        banlist = event["banlist"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"banlist": banlist}))


@receiver(post_save, sender=Notifications)
def notify_update(sender, instance, **kwargs):
    try:
        if instance.content != "test content":
            channel_layer = get_channel_layer()
            res = Notifications.objects.filter(user=instance.user, read=False).order_by(
                "-created_at"
            )
            serializer = notificationsSerializer(res, many=True)
            async_to_sync(channel_layer.group_send)(
                "user_" + str(instance.user.id),
                {"type": "notification_save", "notifications": serializer.data},
            )
            print("user_" + str(instance.user.id), serializer.data)
    except Exception as e:
        print(e)


@receiver(post_save, sender=Blacklist)
def blacklist_update(sender, instance, created, **kwargs):
    try:
        print("blacklist_update")
        channel_layer = get_channel_layer()
        user = instance.user
        if created:
            # autoban
            if instance.post:
                now = timezone.now()
                before = now - timedelta(days=1)
                bls = (
                    Blacklist.objects.filter(
                        blacklist=instance.blacklist, created_at__range=[before, now]
                    )
                    .exclude(post__isnull=True)
                    .count()
                )
                bans = Blacklist.objects.filter(
                    blacklist=instance.blacklist,
                    created_at__range=[before, now],
                    post__isnull=False,
                    status__id=2,
                ).count()
                if bans > 0:
                    instance.status = Status.objects.get(id=7)
                elif bls == 5:
                    instance.status = Status.objects.get(id=2)
                    Blacklist.objects.filter(
                        blacklist=instance.blacklist,
                        created_at__range=[before, now],
                        post__isnull=False,
                        status__id=1,
                    ).update(status=Status.objects.get(id=7))
                    ban = Ban.objects.create(blacklist=instance)
                    ban.save()
            elif instance.comment:
                now = timezone.now()
                before = now - timedelta(days=1)
                bls = (
                    Blacklist.objects.filter(
                        blacklist=instance.blacklist, created_at__range=[before, now]
                    )
                    .exclude(comment__isnull=True)
                    .count()
                )
                bans = Blacklist.objects.filter(
                    blacklist=instance.blacklist,
                    created_at__range=[before, now],
                    comment__isnull=False,
                    status__id=2,
                ).count()
                if bans > 0:
                    instance.status = Status.objects.get(id=7)
                elif bls == 5:
                    instance.status = Status.objects.get(id=2)
                    Blacklist.objects.filter(
                        blacklist=instance.blacklist,
                        created_at__range=[before, now],
                        comment__isnull=False,
                        status__id=1,
                    ).update(status=Status.objects.get(id=7))
                    ban = Ban.objects.create(blacklist=instance)
                    ban.save()
            else:
                now = timezone.now()
                before = now - timedelta(days=1)
                bls = (
                    Blacklist.objects.filter(
                        blacklist=instance.blacklist, created_at__range=[before, now]
                    )
                    .exclude(chat__isnull=True)
                    .count()
                )
                bans = Blacklist.objects.filter(
                    blacklist=instance.blacklist,
                    created_at__range=[before, now],
                    chat__isnull=False,
                    status__id=2,
                ).count()
                if bans > 0:
                    instance.status = Status.objects.get(id=7)
                elif bls == 5:
                    instance.status = Status.objects.get(id=2)
                    Blacklist.objects.filter(
                        blacklist=instance.blacklist,
                        created_at__range=[before, now],
                        chat__isnull=False,
                        status__id=1,
                    ).update(status=Status.objects.get(id=7))
                    ban = Ban.objects.create(blacklist=instance)
                    ban.save()
    except Exception as e:
        print(e)

    # 即時新增使用者blacklist
    try:
        queryset = Blacklist.objects.filter(user=user)
        blacklist = {"article": [], "comment": [], "chat": []}
        for query in queryset:
            if query.post is not None:
                blacklist["article"].append(query.post.id)
            elif query.comment is not None:
                blacklist["comment"].append(query.comment.id)
            elif query.chat is not None:
                blacklist["chat"].append(query.chat.id)
        async_to_sync(channel_layer.group_send)(
            "user_" + str(user.id),
            {"type": "blacklist_save", "blacklist": blacklist},
        )
        print("user_" + str(user.id), blacklist)
    except Exception as e:
        print(e)

    # 依照blacklist新建或更改banlist
    try:
        print("blacklist->banlist")
        if instance.status.id in range(2, 6):
            if instance.post:
                pre = Ban.objects.filter(
                    Q(blacklist__blacklist=user)
                    & Q(end_time__isnull=True)
                    & Q(blacklist__post__isnull=False)
                ).count()
            elif instance.comment:
                pre = Ban.objects.filter(
                    Q(blacklist__blacklist=user)
                    & Q(end_time__isnull=True)
                    & Q(blacklist__comment__isnull=False)
                ).count()
            else:
                pre = Ban.objects.filter(
                    Q(blacklist__blacklist=user)
                    & Q(end_time__isnull=True)
                    & Q(blacklist__chat__isnull=False)
                ).count()
            if pre == 0:
                ban, created = Ban.objects.get_or_create(blacklist=instance)
                if created:
                    ban.start_time = timezone.now()
                if instance.status.id == 2:
                    ban.end_time = ban.start_time + timedelta(days=1)
                elif instance.status.id == 3:
                    ban.end_time = ban.start_time + timedelta(days=15)
                else:
                    ban.end_time = None
                ban.save()
        else:
            ban = Ban.objects.get(blacklist=instance.id)
            ban.end_time = timezone.now()
            ban.save()
    except Exception as e:
        print(e)


# 即時新增使用者banlist
@receiver(post_save, sender=Ban)
def ban_update(sender, instance, created, **kwargs):
    try:
        print("ban_update")
        channel_layer = get_channel_layer()
        user = instance.blacklist.blacklist
        queryset = Ban.objects.filter(
            Q(blacklist__blacklist=user)
            & (Q(end_time__gt=timezone.now()) | Q(end_time__isnull=True))
        )
        banlist = {"article": True, "comment": True, "chat": True}
        if queryset.count() > 0:
            for query in queryset:
                bl = query.blacklist
                if bl.status.name == "停用帳號":
                    banlist = {
                        "article": [
                            bl.status.name,
                            query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        ],
                        "comment": [
                            bl.status.name,
                            query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        ],
                        "chat": [
                            bl.status.name,
                            query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        ],
                    }
                    break
                elif bl.post:
                    banlist["article"] = [
                        bl.status.name,
                        query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                elif bl.comment:
                    banlist["comment"] = [
                        bl.status.name,
                        query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                elif bl.chat:
                    banlist["chat"] = [
                        bl.status.name,
                        query.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    ]
        async_to_sync(channel_layer.group_send)(
            "user_" + str(user.id),
            {"type": "banlist_save", "banlist": banlist},
        )
        print("user_" + str(user.id), banlist)
    except Exception as e:
        print(e)

    # 依照banlist新建或更改notifications
    try:
        print("banlist->notifications")
        bl = instance.blacklist
        if bl.status.name == "禁言24小時":
            if bl.post:
                category = "您發布的文章"
            elif bl.comment:
                category = "您發布的留言"
            else:
                category = "您在聊天室的發言"
            content = (
                category
                + "於短時間內收到多次檢舉，故系統於 "
                + bl.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                + " 起自動禁言24小時<br>我們將同步進行人工審核，若造成不便請見諒，謝謝"
            )
        else:
            content = (
                "經人工審核，因您之前的檢舉違反社群規範，故系統於 "
                + bl.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                + " 起"
                + bl.status.name
                + "<br>若有任何問題，請來信客服信箱，謝謝"
            )
        try:
            notify = Notifications.objects.get(user=bl.blacklist, blacklist=bl)
            notify.content = content
            notify.read = False
            notify.save()
        except Notifications.DoesNotExist:
            Notifications.objects.create(
                user=bl.blacklist, blacklist=bl, content=content
            )
    except Exception as e:
        print(e)
