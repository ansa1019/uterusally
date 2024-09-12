from django.shortcuts import render
from .models import point, gift, exchange, systemPoint
from django.contrib.auth.models import User
from .serializer import (
    PointSerializer,
    GiftSerializer,
    exchangeProductSerializer,
    systemPointSerializer,
)
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

import base64
import datetime

# Create your views here.


class pointView(viewsets.ModelViewSet):
    queryset = point.objects.all()
    serializer_class = PointSerializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user
            response = self.serializer_class(point.objects.filter(user=user), many=True)
            # print("test")
            return Response(response.data)

    """
    如果使用者不存在點數資料，則新增使用者點數資料get_or_create會分出兩個變數，一個是使用者點數資料，一個是是否創建
    如果是就會跑到 if created: 這個條件，然後就會新增使用者點數資料，並且將點數加上去
    如果使用者已經有點數資料，就會跑到 else: 這個條件，然後就會將使用者點數資料的點數加上去
    """
    def create(self, request, *args, **kwargs):
        userPoint, created = point.objects.get_or_create(user=self.request.user)
        if created:
            userPoint.point = userPoint.point + int(self.request.data["point"])
            serializer = self.serializer_class(userPoint)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            up = self.serializer_class(userPoint, data=request.data)
            # print("change")
            if up.is_valid():
                userPoint.point = userPoint.point + int(self.request.data["point"])
                userPoint.save()
                return Response(up.data, status=status.HTTP_201_CREATED)
            else:
                return Response(up.errors, status=status.HTTP_400_BAD_REQUEST)


class giftView(viewsets.ModelViewSet):
    queryset = gift.objects.all()
    serializer_class = GiftSerializer
    """
    如果使用者是匿名使用者，就會回傳{"error": "user is anonymous"}
    如果使用者不是匿名使用者，就會回傳使用者的禮物資料，並且分為兩種情況，一個是使用者是接收者，一個是使用者是贈送者分別為Q(receiver=user) | Q(giver=user)
    
    """

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user
            response = self.serializer_class(
                gift.objects.filter(Q(receiver=user) | Q(giver=user)), many=True
            )
            return Response(response.data)

    def transaction(self, receiverPoint, giverPoint, point):
        receiverPoint.point = receiverPoint.point + int(point)
        receiverPoint.save()

        giverPoint.point = giverPoint.point - int(point)
        giverPoint.save()

    def create(self, request, *args, **kwargs):
        receiver = User.objects.get(username=self.request.data["receiver"])
        receiverPoint, created = point.objects.get_or_create(user=receiver)

        gifter = self.request.user
        giverPoint = point.objects.get(user=gifter)

        if giverPoint.point < int(self.request.data["point"]):
            return Response(
                {"error": "not enough point"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            gift_obj = gift.objects.create(receiver=receiver, giver=gifter)
            serializer = self.serializer_class(gift_obj, data=request.data)
            if created:

                if serializer.is_valid():
                    self.transaction(
                        receiverPoint, giverPoint, int(self.request.data["point"])
                    )
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    receiverPoint.point = receiverPoint.point - int(
                        self.request.data["point"]
                    )
                    receiverPoint.save()
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                if serializer.is_valid():
                    self.transaction(
                        receiverPoint, giverPoint, int(self.request.data["point"])
                    )
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )


class exchangeProductView(viewsets.ModelViewSet):
    queryset = exchange.objects.all()
    serializer_class = exchangeProductSerializer
    """
    這邊是用來檢查使用者是否為匿名使用者，如果是匿名使用者就會回傳{"error": "user is anonymous"}
    如果使用者不是匿名使用者，就會回傳使用者的兌換商品資料，如同giftView
    Create目前是把兌換資料用b64去加密儲存當token，但因為太冗長之後會修改成短寫亂碼來進行非同步兌換
    
    """

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user
            response = self.serializer_class(
                exchange.objects.filter(user=user), many=True
            )
            return Response(response.data)

    def create(self, request, *args, **kwargs):
        from product.models import product

        userPoint = point.objects.get(user=self.request.user)
        product = product.objects.get(product_title=self.request.data["product"])
        amount = int(self.request.data["amount"])

        if userPoint.point < int(product.product_point):
            return Response(
                {"error": "not enough point"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if product.amount == 0:
                return Response(
                    {"error": "product is out of stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            else:
                b64code = (
                    str(self.request.user.username)
                    + product.product_title
                    + str(product.product_point)
                ).encode("UTF-8") + datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ).encode(
                    "UTF-8"
                )
                code = base64.b64encode(b64code).decode("utf-8")
                exchange_obj = exchange.objects.create(
                    user=self.request.user,
                    product=product,
                    point=product.product_point,
                    exchage_token=code,
                    created_at=datetime.datetime.now(),
                    amount=amount,
                )

                serializer = self.serializer_class(exchange_obj, data=request.data)

                if serializer.is_valid():
                    userPoint.point = (
                        userPoint.point - int(product.product_point) * amount
                    )
                    product.amount -= amount
                    product.save()
                    userPoint.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )


class systemPointView(viewsets.ModelViewSet):
    queryset = systemPoint.objects.all()
    serializer_class = systemPointSerializer

    """
    如果之後有bug存在會啟用這個function，之前有想到分割儲存的方式，目前之前的學長有在前端解決分類的問題，之後出錯再來用這邊改
    """

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user
            response = self.serializer_class(
                systemPoint.objects.filter(user=user), many=True
            )
            return Response(response.data)
