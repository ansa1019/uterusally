from django.db import models
from django.contrib.auth.models import User
from product.models import product
import datetime

# Create your models here.


class point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userPoint")
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self):
        return "User:" + self.user.username + "\t" + "Point:" + str(self.point)


class gift(models.Model):
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="giver")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self):
        return (
            "Giver:"
            + self.giver.username
            + "\t"
            + "Receiver:"
            + self.receiver.username
            + "\t"
            + "Point:"
            + str(self.point)
        )


class exchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userExchage")
    exchage_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self):
        return "User:" + self.user.username + "\t" + "Point:" + str(self.point)


class exchangeProducts(models.Model):
    exchange = models.ForeignKey(
        exchange, on_delete=models.CASCADE, related_name="exchange"
    )
    product = models.ForeignKey(
        product, on_delete=models.CASCADE, related_name="productExchage"
    )
    amount = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)


class systemPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="systemPoint")
    task = models.CharField(max_length=255, default="system_task")
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self):
        return (
            "User:"
            + self.user.username
            + "\t"
            + "Task:"
            + self.task
            + "\t"
            + "Point:"
            + str(self.point)
        )
