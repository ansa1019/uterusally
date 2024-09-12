from django.db import models
from django.contrib.auth.models import User
from chat.models import Chat
from content.models import TextEditorPost, TextEditorPostComment
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)


class Blacklist(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, unique=False, blank=True, null=True
    )
    post = models.ForeignKey(
        TextEditorPost, on_delete=models.CASCADE, unique=False, blank=True, null=True
    )
    comment = models.ForeignKey(
        TextEditorPostComment,
        on_delete=models.CASCADE,
        unique=False,
        blank=True,
        null=True,
    )
    blacklist = models.ForeignKey(
        User,
        related_name="blacklist",
        on_delete=models.CASCADE,
        unique=False,
        blank=True,
        null=True,
    )
    reason = models.CharField(max_length=100, unique=False, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default="1")
    created_at = models.DateTimeField(
        auto_now_add=True, auto_created=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, auto_created=True, blank=True, null=True
    )


class Ban(models.Model):
    blacklist = models.ForeignKey(Blacklist, on_delete=models.CASCADE)
    start_time = models.DateTimeField(
        auto_now_add=True, auto_created=True, blank=True, null=True
    )
    end_time = models.DateTimeField(
        auto_created=True,
        blank=True,
        null=True,
    )
