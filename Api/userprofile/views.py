import os
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from content.models import category
from .models import *
from .serializer import *
from .permissions import OwnProfilePermission
from django.contrib.auth.models import User
from .filter.userprofile_filter import personalCalendarFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count


def check_task(queryset, u):
    from task.models import taskRecord, task
    from point.models import point

    not_null = dict()
    count = 0
    no_need = [
        "is_rd",
        "page_music",
        "subscribe",
        "id",
        "created_at",
        "email",
        "user_name",
        "gender",
        "birthday",
        "user_id",
        "nickname",
    ]
    for obj in queryset.values():
        for k in obj.keys():
            if k in no_need:
                continue
            else:
                # obj[k] is not " " or
                if obj[k] is not None:
                    print(type(obj[k]))
                    not_null[k] = False
                else:
                    print(type(obj[k]))
                    print("True")
                    count += 1
                    not_null[k] = True


    t = task.objects.get(title="個人資料")

    try:
        usertask = taskRecord.objects.get(user=u, task=t, is_done=False)
        if usertask.progress != count:
            usertask.progress = count
            usertask.save()
        if all(not_null.values()):
            if usertask.progress == t.progress:
                usertask.is_done = True
                usertask.save()
                up = point.objects.get(user=u)
                up.point += t.point
                up.save()
            else:
                usertask.save()
        return not_null, count
    except:
        usertask = taskRecord.objects.get(user=u, task=t, is_done=True)
        progress = usertask.progress
        return {"task_is_done": "task_is_done"}, progress


class subscribeViewSet(viewsets.ModelViewSet):
    queryset = profile.objects.all()
    serializer_class = profileSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        try:
            subs = User.objects.get(username=request.data["subscribe"])
        except:
            subs = profile.objects.get(nickname=request.data["subscribe"]).user

        sp = profile.objects.get(user=subs)
        if user in sp.subscribe.all():
            sp.subscribe.remove(user)
            sp.save()
            return Response({"status": "unsubscribe success"})
        else:
            sp.subscribe.add(user)
            sp.save()
            return Response({"status": "subscribe success"})

    def list(self, request, *args, **kwargs):
        user = self.request.user

        query = self.queryset.filter(subscribe=user)
        subs = []
        for q in query.values():
            subs.append([{"nickname": q["nickname"]}])
        return Response({"subscribe": subs})


class profileViewSet(viewsets.ModelViewSet):
    queryset = profile.objects.all()
    serializer_class = profileSerializer
    permission_classes = [OwnProfilePermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        is_null, count = check_task(queryset, request.user)
        serializer_data = list(serializer.data)
        serializer_data.append({"is_null": is_null})
        serializer_data.append({"blank": count})
        return Response(serializer_data)

    def update(self, request, *args, **kwargs):
        user = request.user
        profile_obj = profile.objects.filter(user=user)

        if "user_image" in request.data:
            try:
                old_file = profile_obj[0].user_image.path
                if os.path.isfile(old_file):
                    os.remove(old_file)
            except:
                pass

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        res = dict()
        profile_is_true, pc = check_task(profile_obj, user)
        res.update({"status": "update success"})
        res.update({"blank": pc})
        res.update(profile_is_true)
        return Response([serializer.data, res])


class bodyProfileViewSet(viewsets.ModelViewSet):
    queryset = bodyProfile.objects.all()
    serializer_class = bodyProfileSerializer
    permission_classes = [OwnProfilePermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class personalCalendarViewSet(viewsets.ModelViewSet):
    queryset = personal_calendar.objects.all()
    serializer_class = personalCalendarSerializer
    filter_class = personalCalendarFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # permission_classes = [OwnProfilePermission]

    def list(self, request, *args, **kwargs):
        u = User.objects.get(username=request.user)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=u)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     date = kwargs['date']
    #     print(date)
    #     try:
    #         u = User.objects.get(username=request.user)
    #         queryset = self.filter_queryset(self.get_queryset())
    #
    #         date = self.request.query_params.get('date')
    #         print(date)
    #         print([True if date is not None else False])
    #         if date is not None:
    #             today = now().date()
    #             queryset = queryset.filter(user=u, date__gte=today).order_by('date')[::-1]
    #             print(queryset)
    #             serializer = self.get_serializer(queryset, many=True)
    #             print(serializer.data)
    #             return Response(serializer.data)
    #         else:
    #             return Response({'status': 'no date'})
    #
    #     except:
    #         return Response({'status': 'user not found'})

    def filter_queryset(self, queryset):
        if self.request.query_params.get("today", None) == "":
            for backend in list(self.filter_backends):
                queryset = backend().filter_queryset(self.request, queryset, self)
            return queryset
        else:
            try:
                queryset = queryset.filter(
                    date__gte=self.request.query_params.get("today", None)
                )
                return queryset
            except ValidationError:
                for backend in list(self.filter_backends):
                    queryset = backend().filter_queryset(self.request, queryset, self)
                return queryset
            except ValueError:
                for backend in list(self.filter_backends):
                    queryset = backend().filter_queryset(self.request, queryset, self)
                return queryset


class subPersonalCalendarViewSet(viewsets.ModelViewSet):
    queryset = subPersonalCalendar.objects.all()
    serializer_class = subPersonalCalendarSerializer
    # permission_classes = [OwnProfilePermission]

    def list(self, request, *args, **kwargs):
        u = User.objects.get(username=request.user)
        # try:
        c = personal_calendar.objects.filter(user=u)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(calendar__in=c)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # except:
        #     response = {'status': 'no calendar'}
        #     return Response(response)


class getUserSubscribeViewSet(viewsets.ModelViewSet):
    queryset = profile.objects.all()
    serializer_class = profileSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        profile_obj = profile.objects.get(user=user)
        subs = []

        for sub in profile_obj.subscribe.all():
            subs.append(sub.username)
        return Response({"subscribe": subs})


class subTopicViewSet(viewsets.ModelViewSet):
    queryset = subscribeTopic.objects.all()
    serializer_class = subscribeTopicSerializer
    # permission_classes = [OwnProfilePermission]

    def create(self, request, *args, **kwargs):
        cate = request.data.get("category")
        cate = category.objects.get(name=cate)
        user = request.user
        queryset, created = self.queryset.get_or_create(user=user)
        # print(queryset, created)
        if cate in queryset.topic.all():
            queryset.topic.remove(cate)
            return Response({"status": "unsubscribe success"})
        else:
            queryset.topic.add(cate)
            return Response({"status": "subscribe success"})

    def list(self, request, *args, **kwargs):

        u = User.objects.get(username=request.user)
        queryset = self.queryset.filter(user=u)
        if not queryset:
            obj = subscribeTopic.objects.create(user=u)
            obj.save()
            queryset = self.queryset.filter(user=u)
            # print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class recommendUserViewSet(viewsets.ModelViewSet):
    queryset = profile.objects.all()
    serializer_class = profileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        queryset = queryset.annotate(subscribe_count=Count("subscribe")).order_by(
            "-subscribe_count"
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class subscribeHashtagViewSet(viewsets.ModelViewSet):
    queryset = subscribeHashtag.objects.all()
    serializer_class = subscribeHashtagSerializer
    # permission_classes = [OwnProfilePermission]

    def create(self, request, *args, **kwargs):
        hashtag = request.data.get("hashtag")
        user = request.user
        queryset, created = self.queryset.get_or_create(user=user, hashtag=hashtag)
        if created:
            return Response({"status": "subscribe success"})
        else:
            # print(queryset)
            queryset.delete()
            return Response({"status": "unsubscribe success"})

    def list(self, request, *args, **kwargs):
        u = User.objects.get(username=request.user)
        hashtags = []
        queryset = self.queryset.filter(user=u)
        queryset = queryset.values("hashtag")
        for hashtag in queryset:
            hashtags.append(hashtag["hashtag"])
        return Response({"subHashtag": hashtags})
