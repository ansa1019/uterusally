from rest_framework import serializers
from .models import *
from product.models import product
from product.serializer import productSerializer
import base64
from django.contrib.auth.models import User
import datetime


class PointSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = point
        fields = "__all__"


class GiftSerializer(serializers.ModelSerializer):
    giver = serializers.CharField(read_only=True)
    receiver = serializers.SerializerMethodField("get_receiver")

    class Meta:
        model = gift
        fields = "__all__"

    def get_receiver(self, obj):
        return obj.receiver.username


class exchangeProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = exchangeProducts
        fields = "__all__"


class exchangeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("get_products")
    point = serializers.SerializerMethodField("get_point")

    class Meta:
        model = exchange
        fields = "__all__"

    def get_products(self, obj):
        products = []
        for pro in exchangeProducts.objects.filter(exchange=obj):
            products.append(
                {
                    "product": pro.product.product_title,
                    "amount": pro.amount,
                    "point": pro.point,
                }
            )
        return products

    def get_point(self, obj):
        point = 0
        for pro in exchangeProducts.objects.filter(exchange=obj):
            point += pro.point
        return point


class systemPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = systemPoint
        fields = "__all__"
