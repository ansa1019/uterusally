from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from notifications.models import Notifications
from .models import task, taskRecord
from .serializer import TaskSerializer, TaskRecordSerializer

# Create your views here.


class taskViewSet(viewsets.ModelViewSet):
    queryset = task.objects.all()
    serializer_class = TaskSerializer


class taskRecordViewSet(viewsets.ModelViewSet):
    queryset = taskRecord.objects.all()
    serializer_class = TaskRecordSerializer
    ordering_fields = ["task__title", "is_done", "progress"]
    """
    這邊會自動寫入taskRecord資料表，如果使用者沒有任務資料，就會新增任務資料
    taskRecord資料表是用來記錄使用者的任務進度，如果使用者完成任務，就會將任務的進度加上去
    如果任務的進度等於任務的進度，就會將使用者的點數加上去
    這邊apscheduler會每天更新任務的進度，如果任務是每日任務，就會將進度歸零
    但現在可以使用celelry來更新任務的進度，這部分還沒改，這邊會改為使用celery是因為celery可以更好的處理任務，如果有需要看使用率，\
    celery可以更好的處理
    """

    def list(self, request, *args, **kwargs):
        from .models import task
        from userprofile.models import profile
        from userprofile.views import check_task

        begginer_task = task.objects.filter(type="BEGGINER")
        dayly_task = task.objects.filter(type="DAILY")
        event_task = task.objects.filter(Q(type="EVENT") & Q(is_active=True))
        queryset = taskRecord.objects.filter(user=request.user)

        if (
            queryset.exclude(Q(task__in=dayly_task) | Q(task__in=event_task))
            and queryset.filter(task__in=begginer_task).count()
            == task.objects.filter(type="BEGGINER").count()
        ):
            pass
        else:
            for task in begginer_task:
                if task.title not in queryset.values_list("task__title", flat=True):
                    taskRecord.objects.create(user=request.user, task=task)

        if (
            queryset.exclude(Q(task__in=begginer_task) | Q(task__in=event_task))
            and queryset.filter(task__in=dayly_task).count()
            == task.objects.filter(type="DAILY").count()
        ):
            pass
        else:
            for task in dayly_task:
                if task.title not in queryset.values_list("task__title", flat=True):
                    taskRecord.objects.create(user=request.user, task=task)

        if queryset.exclude(
            Q(task__in=begginer_task) | Q(task__in=dayly_task)
        ) not in task.objects.filter(Q(type="EVENT") & Q(is_active=True)):
            for task in event_task:
                if task.title not in queryset.values_list("task__title", flat=True):
                    taskRecord.objects.create(user=request.user, task=task)
        queryset = taskRecord.objects.filter(user=request.user)
        serializer = TaskRecordSerializer(queryset, many=True)
        userProfile = profile.objects.filter(user=request.user)
        is_null, count = check_task(userProfile, request.user)
        serializer_data = list(serializer.data)
        serializer_data.append({"profile": {"is_null": is_null, "count": count}})
        # print(serializer_data)
        return Response(serializer_data)

    def create(self, request, *args, **kwargs):
        from .models import task
        from point.models import point, systemPoint

        t = task.objects.get(title=self.request.data["task_title"], is_active=True)
        record, created = taskRecord.objects.get_or_create(user=request.user, task=t)

        try:
            record.progress += int(self.request.data["progress"])
        except:
            record.progress += 1

        record.save()

        if record.progress == t.progress:
            userPoint = point.objects.get(user=self.request.user)
            userPoint.point = userPoint.point + t.point
            userPoint.save()

            record.is_done = True
            record.save()

            serializer = TaskRecordSerializer(record)

            system_task_record = systemPoint.objects.create(
                user=self.request.user,
                point=t.point,
                task=self.request.data["task_title"],
            )
            system_task_record.save()

            poi = point.objects.get(user=request.user)
            content = "您已完成 # 任務，獲得點數 # 點，目前點數 # 點！"
            notify = Notifications.objects.create(
                user=request.user,
                systemPoint=system_task_record,
                content=content.replace("#", request.data["task_title"])
                .replace("#", system_task_record.point)
                .replace("#", poi.point),
            )

            return Response(serializer.data)
        else:
            serializer = TaskRecordSerializer(record)
            # print(serializer.data)
            return Response(serializer.data)


def task_update(type_of_task):
    """
    目前是給apscheduler使用，但現在可以使用celery來更新任務的進度，可以無痛直接給celery使用
    """
    match type_of_task:
        case "DAILY":
            # print("DAILY is update")
            ts = task.objects.filter(type=type_of_task)
            for t in ts:
                taskRecord.objects.filter(task=t).update(progress=0, is_done=False)

        case "WEEKLY":
            taskRecord.objects.filter(type=type_of_task).update(
                progress=0, is_done=False
            )

        case "EVENT":
            taskRecord.objects.filter(type=type_of_task).update(
                progress=0, is_done=False
            )
