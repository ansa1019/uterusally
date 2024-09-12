from django.db import models
from django.contrib.auth.models import User
from content.models import TextEditorPost

# Create your models here.

class postStoraged(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    storage_name = models.CharField(max_length=255, blank=True, null=True, default="未命名資料夾")
    post = models.ManyToManyField(TextEditorPost, related_name="postStoraged", blank=True)

    def __str__(self):
        return "資料夾名稱 : " + self.storage_name + "使用者 : " + self.user.username