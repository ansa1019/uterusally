from django.db import models
from django.contrib.auth.models import User
from content.models import TextEditorPost
# Create your models here.

TYPE_CHOICES = (
    ("BEGGINER", "beginner"),
    ("WEEKLY", "weekly"),
    ("DAILY", "daily"),
    ("EVENT", "event"),
)


REQUIREMENT_CHOICES = (
    ("LIKE", 10),
    ("SHARE", 10),
    ("OTHER", 10),
)


class task(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True, unique=True)
    point = models.PositiveIntegerField(default=0, null=True, blank=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, null=True, blank=True, default="")
    progress = models.PositiveIntegerField(default=0, null=True, blank=True,)
    deadline = models.DateTimeField(null=True, blank=True,)
    requirement = models.CharField(max_length=100, null=True, blank=True, default="")
    specify_content = models.ForeignKey(TextEditorPost, on_delete=models.CASCADE, null=True, blank=True, )
    is_active = models.BooleanField(default=True, null=True, blank=True,)

    def __str__(self):
        return self.title + '\t' + 'typeof:' + self.type + '\t' + 'point:' + str(self.point)


class taskRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    task = models.ForeignKey(task, on_delete=models.CASCADE, null=True, blank=True,)
    progress = models.PositiveIntegerField(default=0, null=True, blank=True, )
    is_done = models.BooleanField(default=False, null=True, blank=True,)

    def __str__(self):
        return 'title:' + self.task.title + '\t' + 'user:' + self.user.username + '\t' + 'is_done:' + str(self.is_done)