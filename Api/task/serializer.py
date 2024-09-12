from rest_framework import serializers
from .models import task, taskRecord


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = '__all__'


class TaskRecordSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', write_only=True)
    task_type = serializers.CharField(source='task.type', read_only=True)
    task_deadline = serializers.DateTimeField(source='task.deadline', read_only=True)
    task_point = serializers.IntegerField(source='task.point', read_only=True)
    task = serializers.CharField(source='task.title', read_only=True)
    task_progress = serializers.IntegerField(source='task.progress', read_only=True)
    requirement = serializers.SerializerMethodField('get_task')
    is_done = serializers.BooleanField(read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)



    class Meta:
        model = taskRecord
        fields = '__all__'


    def get_task(self, obj):
        return obj.task.requirement
