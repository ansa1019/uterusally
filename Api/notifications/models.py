from django.db import models
from django.contrib.auth.models import User
from userprofile.models import subscribeHashtag
from content.models import TextEditorPost, TextEditorPostComment
from blacklist.models import Blacklist
from product.models import product
from point.models import *

# Create your models here.


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default="test content")
    author = models.ForeignKey(
        User, related_name="author", on_delete=models.CASCADE, null=True, blank=True
    )
    hashtag = models.ForeignKey(
        subscribeHashtag, on_delete=models.CASCADE, null=True, blank=True
    )
    post = models.ForeignKey(
        TextEditorPost, on_delete=models.CASCADE, null=True, blank=True
    )
    comment = models.ForeignKey(
        TextEditorPostComment, on_delete=models.CASCADE, null=True, blank=True
    )
    gift = models.ForeignKey(gift, on_delete=models.CASCADE, null=True, blank=True)
    exchange = models.ForeignKey(
        exchange, on_delete=models.CASCADE, null=True, blank=True
    )
    systemPoint = models.ForeignKey(
        systemPoint, on_delete=models.CASCADE, null=True, blank=True
    )
    blacklist = models.ForeignKey(
        Blacklist, on_delete=models.CASCADE, null=True, blank=True
    )
    product = models.ForeignKey(
        product, on_delete=models.CASCADE, null=True, blank=True
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_created=True, null=True, blank=True
    )
