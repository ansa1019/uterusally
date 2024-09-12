from rest_framework import serializers
from .models import point, gift, exchange, systemPoint
from product.models import product
from product.serializer import productSerializer
import base64
from django.contrib.auth.models import User
import datetime


class PointSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model = point
        fields = '__all__'


class GiftSerializer(serializers.ModelSerializer):
    giver = serializers.CharField(read_only=True)
    receiver = serializers.SerializerMethodField('get_receiver')
    class Meta:
        model = gift
        fields = '__all__'

    def get_receiver(self, obj):
        return obj.receiver.username


class exchangeProductSerializer(serializers.ModelSerializer):
    exchage_token = serializers.CharField(read_only=True)
    product_title = serializers.SerializerMethodField('get_product_title')
    product = serializers.SerializerMethodField('get_product')
    point = serializers.IntegerField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = exchange
        fields = '__all__'

    def get_product_title(self, obj):
        return obj.product.product_title

    def get_product(self, obj):
        return obj.product.id


class systemPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = systemPoint
        fields = '__all__'