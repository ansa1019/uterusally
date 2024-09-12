from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    room = models.CharField(max_length=100, unique=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identity = models.CharField(max_length=100, unique=False, blank=True, null=True)
    message = models.TextField(default="test message")
    desable = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_created=True, null=True, blank=True
    )
